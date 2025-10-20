import pytest
from fastapi.testclient import TestClient
from routes.fornecedor.fornecedor_planos import router
from main import app
from data.plano import plano_repo

app.include_router(router)
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Garante que a tabela plano existe antes dos testes
    plano_repo.criar_tabela_plano()

@pytest.fixture
def fornecedor_id():
    # Use um id fixo ou mock conforme necessário
    return 1

# Teste: Não permite assinar plano se já houver assinatura ativa
def test_assinar_plano_com_assinatura_ativa(monkeypatch, fornecedor_id):
    def mock_obter_assinatura_ativa_por_fornecedor(id_fornecedor):
        return True  # Simula assinatura ativa
    monkeypatch.setattr(
        "data.inscricaoplano.inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor",
        mock_obter_assinatura_ativa_por_fornecedor
    )
    response = client.post("/fornecedor/planos/assinar", data={"plano_id": "1", "id_fornecedor": fornecedor_id})
    assert "assinatura ativa" in response.text

# Teste: Não permite cancelar plano se não houver assinatura ativa
def test_cancelar_plano_sem_assinatura_ativa(monkeypatch, fornecedor_id):
    def mock_obter_assinatura_ativa_por_fornecedor(id_fornecedor):
        return None  # Simula sem assinatura ativa
    monkeypatch.setattr(
        "data.inscricaoplano.inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor",
        mock_obter_assinatura_ativa_por_fornecedor
    )
    response = client.post("/fornecedor/planos/cancelar", data={"id_fornecedor": fornecedor_id, "confirmacao": "confirmar"})
    assert "assinatura ativa" in response.text

# Teste: Não permite renovar plano se não houver assinatura ativa
def test_renovar_plano_sem_assinatura_ativa(monkeypatch, fornecedor_id):
    def mock_obter_assinatura_ativa_por_fornecedor(id_fornecedor):
        return None
    monkeypatch.setattr(
        "data.inscricaoplano.inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor",
        mock_obter_assinatura_ativa_por_fornecedor
    )
    response = client.post("/fornecedor/planos/renovar", data={"plano_id": "1", "id_fornecedor": fornecedor_id})
    assert "assinatura ativa" in response.text

# Teste: Não permite alterar plano se não houver assinatura ativa
def test_alterar_plano_sem_assinatura_ativa(monkeypatch, fornecedor_id):
    def mock_obter_assinatura_ativa_por_fornecedor(id_fornecedor):
        return None
    monkeypatch.setattr(
        "data.inscricaoplano.inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor",
        mock_obter_assinatura_ativa_por_fornecedor
    )
    response = client.post("/fornecedor/planos/alterar", data={"id_plano": "1", "id_fornecedor": fornecedor_id})
    assert "assinatura ativa" in response.text
