import pytest
import os
import sys
import tempfile
import gc
import uuid
from util import db as db_module

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture()
def test_db():
    # CRITICAL FIX: Reset global connection pool before each test
    # This ensures each test gets a clean pool pointing to its own database
    if db_module._connection_pool is not None:
        db_module._connection_pool.close_all()
    db_module._connection_pool = None

    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path
    # Fecha todas as conexões do pool antes de limpar
    if db_module._connection_pool is not None:
        db_module._connection_pool.close_all()
    db_module._connection_pool = None
    # Força fechamento de conexões SQLite
    gc.collect()
    # Remove o arquivo temporário ao concluir o teste
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except PermissionError:
            pass


@pytest.fixture
def email_unico():
    """
    Gera um email único para cada teste.
    Útil para evitar violações de UNIQUE constraint.

    Uso:
        def test_inserir_usuario(test_db, email_unico):
            usuario = Usuario(email=email_unico, ...)
    """
    return f"teste_{uuid.uuid4().hex[:8]}@teste.com"


@pytest.fixture
def cpf_unico():
    """
    Gera um CPF único (formato válido) para cada teste.

    Nota: Este é um CPF sintaticamente válido, mas não real.
    """
    # Gera 9 dígitos aleatórios
    import random
    base = ''.join([str(random.randint(0, 9)) for _ in range(9)])

    # Calcula primeiro dígito verificador
    soma = sum(int(base[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10

    # Calcula segundo dígito verificador
    base_com_d1 = base + str(d1)
    soma = sum(int(base_com_d1[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10

    return base + str(d1) + str(d2)


@pytest.fixture
def dados_usuario_unico(email_unico, cpf_unico):
    """
    Retorna um dicionário com dados únicos para criar usuário de teste.

    Uso:
        def test_criar_usuario(test_db, dados_usuario_unico):
            usuario = Usuario(**dados_usuario_unico)
    """
    return {
        "email": email_unico,
        "cpf_cnpj": cpf_unico,
        "nome": "Usuário Teste",
        "senha": "senha123",
        "telefone": "27999999999",
        "cep": "29100-000",
        "rua": "Rua Teste",
        "numero": "123",
        "complemento": "",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "estado": "ES",
        "tipo_usuario": "cliente"
    }
