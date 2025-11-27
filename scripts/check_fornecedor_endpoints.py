from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

routes = [
    "/fornecedor",
    "/fornecedor/perfil",
    "/fornecedor/produtos/listar",
    "/fornecedor/solicitacoes_recebidas",
    "/fornecedor/mensagens/recebidas",
    "/fornecedor/avaliacoes",
]

for r in routes:
    try:
        resp = client.get(r)
        print(r, resp.status_code)
    except Exception as e:
        print(r, 'ERROR', str(e))
