import sqlite3
import os
from datetime import datetime
import logging
from queue import Queue, Empty
from contextlib import contextmanager
import threading

logger = logging.getLogger(__name__)


class SQLiteConnectionPool:
    """
    Pool de conexões simples para SQLite.
    Reutiliza conexões ao invés de criar novas a cada operação.

    Para uso acadêmico - ajuda com performance mas SQLite não é ideal para alta concorrência.
    """

    def __init__(self, database_path: str, max_connections: int = 5):
        """
        Inicializa o pool de conexões.

        Args:
            database_path: Caminho do banco de dados
            max_connections: Número máximo de conexões no pool
        """
        self.database_path = database_path
        self.max_connections = max_connections
        self._pool: Queue = Queue(maxsize=max_connections)
        self._all_connections = []
        self._lock = threading.Lock()

        # Pré-criar conexões
        for _ in range(max_connections):
            conn = self._create_connection()
            self._pool.put(conn)
            self._all_connections.append(conn)

        logger.info(f"Pool de conexões criado com {max_connections} conexões")

    def _create_connection(self) -> sqlite3.Connection:
        """Cria uma nova conexão com as configurações corretas"""
        conn = sqlite3.connect(
            self.database_path,
            check_same_thread=False,
            timeout=30.0  # Timeout de 30 segundos para evitar database is locked
        )
        conn.row_factory = sqlite3.Row
        # Habilitar WAL mode para melhor concorrência
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")  # 30 segundos em milissegundos
        except:
            pass
        return conn

    @contextmanager
    def get_connection(self):
        """
        Context manager para obter uma conexão do pool.

        Exemplo:
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario")
        """
        conn = None
        try:
            # Tentar obter conexão do pool (timeout de 5 segundos)
            conn = self._pool.get(timeout=5)
            yield conn
        except Empty:
            logger.warning("Pool de conexões esgotado, criando conexão temporária")
            # Se pool esgotado, criar conexão temporária
            conn = self._create_connection()
            yield conn
        finally:
            if conn is not None:
                try:
                    # Devolver conexão ao pool
                    self._pool.put_nowait(conn)
                except:
                    # Se pool cheio, fechar conexão temporária
                    conn.close()

    def close_all(self):
        """Fecha todas as conexões do pool"""
        with self._lock:
            for conn in self._all_connections:
                try:
                    conn.close()
                except:
                    pass
            logger.info("Todas as conexões do pool foram fechadas")


# Instância global do pool
_connection_pool = None


def get_pool() -> SQLiteConnectionPool:
    """Obtém ou cria a instância global do pool de conexões"""
    global _connection_pool
    if _connection_pool is None:
        database_path = os.environ.get('TEST_DATABASE_PATH', 'obratto.db')
        _connection_pool = SQLiteConnectionPool(database_path, max_connections=5)
    return _connection_pool


def open_connection():
    """
    Abre conexão com o banco de dados usando o pool de conexões.

    IMPORTANTE: Use sempre com context manager:
        with open_connection() as conn:
            # usar conexão
    """
    return get_pool().get_connection()

def get_database_info():
    """Retorna informações sobre o banco de dados"""
    try:
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            return {
                'database_file': 'obratto.db',
                'tables': tables,
                'status': 'connected'
            }
    except Exception as e:
        return {
            'database_file': 'obratto.db',
            'tables': [],
            'status': f'error: {str(e)}'
        }

def seed_usuarios_padrao():
    """Cria usuários padrão para cada perfil caso ainda não existam."""
    from util.security import criar_hash_senha

    perfis = ['administrador', 'cliente', 'fornecedor', 'prestador']
    senha_padrao = '1234aA@#'
    senha_hash = criar_hash_senha(senha_padrao)

    try:
        with open_connection() as conn:
            cursor = conn.cursor()

            for perfil in perfis:
                email = f'padrao@{perfil}.com'

                # Verificar se já existe um usuário com este email
                cursor.execute("SELECT id FROM usuario WHERE email = ?", (email,))
                usuario_existente = cursor.fetchone()

                if not usuario_existente:
                    # Criar usuário padrão
                    data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("""
                        INSERT INTO usuario (
                            nome, email, senha, cpf_cnpj, telefone,
                            cep, rua, numero, complemento, bairro,
                            cidade, estado, data_cadastro, tipo_usuario
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f'Usuário {perfil.capitalize()}',
                        email,
                        senha_hash,
                        '00000000000' if perfil in ['administrador', 'cliente', 'prestador'] else '00000000000000',
                        '00000000000',
                        '00000-000',
                        'Rua Padrão',
                        '0',
                        '',
                        'Bairro Padrão',
                        'Cidade Padrão',
                        'ES',
                        data_cadastro,
                        perfil
                    ))

                    usuario_id = cursor.lastrowid

                    # Criar registro na tabela específica do perfil
                    if perfil == 'administrador':
                        cursor.execute("""
                            INSERT INTO administrador (id_usuario)
                            VALUES (?)
                        """, (usuario_id,))
                    elif perfil == 'cliente':
                        cursor.execute("""
                            INSERT INTO cliente (id, genero, data_nascimento)
                            VALUES (?, ?, ?)
                        """, (usuario_id, 'Não Informado', '2000-01-01'))
                    elif perfil == 'fornecedor':
                        cursor.execute("""
                            INSERT INTO fornecedor (id, razao_social, selo_confianca)
                            VALUES (?, ?, ?)
                        """, (usuario_id, 'Fornecedor Padrão', 0))
                    elif perfil == 'prestador':
                        cursor.execute("""
                            INSERT INTO prestador (id, area_atuacao, razao_social, descricao_servicos, selo_confianca)
                            VALUES (?, ?, ?, ?, ?)
                        """, (usuario_id, 'Área Padrão', 'Prestador Padrão', 'Serviços Padrão', 0))

                    logger.info(f"Usuário padrão criado: {email}")
                else:
                    logger.debug(f"Usuário padrão já existe: {email}")

            conn.commit()
            logger.info("Seed de usuários padrão concluído com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao criar usuários padrão: {e}", exc_info=True)