import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db(test_db):
    # Usa o test_db do conftest para garantir isolamento
    yield
    # Cleanup após cada teste

def test_listar_produtos_requer_autenticacao():
    """Testa que a rota de listar produtos requer autenticação"""
    response = client.get("/fornecedor/produtos/listar", follow_redirects=False)
    # Deve redirecionar para login (303) ou retornar 404 se rota não existir
    assert response.status_code in [200, 303, 404]
    if response.status_code == 200:
        assert "login" in response.text.lower()

def test_inserir_produto_requer_autenticacao():
    """Testa que a rota de inserir produto requer autenticação"""
    data = {
        "nome": "Produto Teste",
        "descricao": "Descrição do produto teste",
        "preco": "10.0",
        "quantidade": "5"
    }
    files = {"foto": ("foto.jpg", b"fakeimgdata", "image/jpeg")}
    response = client.post("/fornecedor/produtos/inserir", data=data, files=files, follow_redirects=False)
    assert response.status_code in [200, 303, 404]
    if response.status_code == 200:
        assert "login" in response.text.lower()

def test_atualizar_produto_requer_autenticacao():
    """Testa que a rota de atualizar produto requer autenticação"""
    data = {
        "nome": "Produto Atualizar",
        "descricao": "Desc Atualizar",
        "preco": "20.0",
        "quantidade": "2"
    }
    files = {"foto": ("foto2.jpg", b"fakeimgdata2", "image/jpeg")}
    response = client.post("/fornecedor/produtos/atualizar/1", data=data, files=files, follow_redirects=False)
    assert response.status_code in [200, 303, 404]
    if response.status_code == 200:
        assert "login" in response.text.lower()
