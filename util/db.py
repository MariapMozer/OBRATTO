import sqlite3
import os
from datetime import datetime


def open_connection():
    """Abre conexão com o banco de dados obratto.db, garantindo fechamento correto."""
    database_path = os.environ.get('TEST_DATABASE_PATH', 'obratto.db')
    conexao = sqlite3.connect(database_path, check_same_thread=False)
    conexao.row_factory = sqlite3.Row
    return conexao

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

                    print(f"Usuário padrão criado: {email}")
                else:
                    print(f"Usuário padrão já existe: {email}")

            conn.commit()
            print("Seed de usuários padrão concluído com sucesso!")

    except Exception as e:
        print(f"Erro ao criar usuários padrão: {e}")