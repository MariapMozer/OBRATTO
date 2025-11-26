import pytest
from fastapi.testclient import TestClient
from main import app
from data.plano import plano_repo

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db(test_db):
    # Garante que a tabela plano existe antes dos testes
    # test_db é do conftest.py e garante isolamento
    plano_repo.criar_tabela_plano()
    yield
    # Cleanup após cada teste

# Teste: Verifica que rotas de planos requerem autenticação
def test_listar_planos_requer_autenticacao():
    """Testa que a rota de listar planos requer autenticação"""
    response = client.get("/fornecedor/planos/listar", follow_redirects=False)
    # Deve redirecionar para login (303) ou retornar página de login (200 com HTML de login)
    assert response.status_code in [200, 303]
    if response.status_code == 200:
        assert "login" in response.text.lower()

def test_meu_plano_requer_autenticacao():
    """Testa que a rota de ver meu plano requer autenticação"""
    response = client.get("/fornecedor/planos/meu_plano?id_fornecedor=1", follow_redirects=False)
    assert response.status_code in [200, 303]
    if response.status_code == 200:
        assert "login" in response.text.lower()

def test_alterar_plano_get_requer_autenticacao():
    """Testa que a rota GET de alterar plano requer autenticação"""
    response = client.get("/fornecedor/planos/alterar?id_fornecedor=1", follow_redirects=False)
    assert response.status_code in [200, 303]
    if response.status_code == 200:
        assert "login" in response.text.lower()

def test_alterar_plano_post_requer_autenticacao():
    """Testa que a rota POST de alterar plano requer autenticação"""
    response = client.post("/fornecedor/planos/alterar",
                          data={"id_plano": "1", "id_fornecedor": "1"},
                          follow_redirects=False)
    assert response.status_code in [200, 303]
    if response.status_code == 200:
        assert "login" in response.text.lower()
