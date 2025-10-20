import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_form():
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

def test_cadastrar_usuario_cliente():
    response = client.post("/cadastro/cliente", data={
        "nome": "Teste Cliente",
        "email": "cliente_test@teste.com",
        "senha": "123456",
        "confirmar_senha": "123456",
        "cpf_cnpj": "12345678900",
        "telefone": "11999999999",
        "cep": "29000-000",
        "estado": "ES",
        "cidade": "Vitória",
        "rua": "Rua Teste",
        "numero": "123",
        "bairro": "Centro",
        "complemento": "",
        "genero": "M",
        "data_nascimento": "2000-01-01"
    })
    # Expects redirect to /login on success
    assert response.status_code in [200, 303]

def test_cadastrar_usuario_fornecedor():
    response = client.post("/cadastro/fornecedor", data={
        "nome": "Teste Fornecedor",
        "email": "fornecedor_test@teste.com",
        "senha": "123456",
        "confirmar_senha": "123456",
        "cpf_cnpj": "12345678901234",
        "telefone": "11988888888",
        "cep": "29000-000",
        "estado": "ES",
        "cidade": "Vitória",
        "rua": "Rua Fornecedor",
        "numero": "456",
        "bairro": "Centro",
        "complemento": "",
        "razao_social": "Fornecedor Teste"
    })
    # Expects redirect to /login on success
    assert response.status_code in [200, 303]

def test_cadastrar_usuario_prestador():
    response = client.post("/cadastro/prestador", data={
        "nomeCompleto": "Teste Prestador",
        "email": "prestador_test@teste.com",
        "senha": "123456",
        "confirmarSenha": "123456",
        "documento": "12345678902",
        "telefone": "11977777777",
        "cep": "29000-000",
        "estado": "ES",
        "cidade": "Vitória",
        "rua": "Rua Prestador",
        "numero": "789",
        "bairro": "Centro",
        "complemento": "",
        "area_atuacao": "TI",
        "razao_social": "Prestador Teste",
        "descricao_servicos": "Serviços de TI"
    })
    # Expects redirect to /login on success
    assert response.status_code in [200, 303]

def test_login_post():
    """Test POST to login route"""
    response = client.post("/login", data={
        "email": "test@example.com",
        "senha": "wrongpassword"
    })
    # Should return 401 for invalid credentials or 200 showing login form with error
    assert response.status_code in [200, 401]

def test_logout():
    """Test logout route"""
    response = client.get("/logout", follow_redirects=False)
    # Should redirect to home
    assert response.status_code == 303

def test_escolha_cadastro():
    """Test route to choose registration type"""
    response = client.get("/escolha_cadastro")
    assert response.status_code == 200

def test_recuperar_senha_get():
    """Test password recovery form"""
    response = client.get("/recuperar-senha")
    assert response.status_code == 200
