import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Exemplo de login de fornecedor (ajuste conforme seu fluxo de autenticação)
def login_fornecedor():
    response = client.post("/entrar", data={
        "email": "fornecedor1@teste.com",
        "senha": "fornecedor123"
    })
    assert response.status_code in (200, 303)
    # Retorna cookies de sessão para requests autenticados
    return response.cookies

def test_listar_produtos():
    cookies = login_fornecedor()
    response = client.get("/fornecedor/produtos/listar", cookies=cookies)
    assert response.status_code == 200
    assert "produtos" in response.text

def test_inserir_produto():
    cookies = login_fornecedor()
    data = {
        "nome": "Produto Teste",
        "descricao": "Descrição do produto teste",
        "preco": "10.0",
        "quantidade": "5"
    }
    files = {"foto": ("foto.jpg", b"fakeimgdata", "image/jpeg")}
    response = client.post("/fornecedor/produtos/inserir", data=data, files=files, cookies=cookies)
    assert response.status_code == 200 or response.status_code == 303
    assert "Produto inserido com sucesso" in response.text

def test_atualizar_produto():
    cookies = login_fornecedor()
    # Primeiro, insere um produto para garantir que existe
    data = {
        "nome": "Produto Atualizar",
        "descricao": "Desc Atualizar",
        "preco": "20.0",
        "quantidade": "2"
    }
    files = {"foto": ("foto2.jpg", b"fakeimgdata2", "image/jpeg")}
    insert_resp = client.post("/fornecedor/produtos/inserir", data=data, files=files, cookies=cookies)
    assert insert_resp.status_code == 200 or insert_resp.status_code == 303
    # Busca o id do produto inserido (ajuste conforme seu template/retorno)
    # Aqui é um exemplo genérico:
    # produto_id = ...
    # response = client.post(f"/fornecedor/produtos/atualizar/{produto_id}", ...)
    # assert response.status_code == 200

# Adicione outros testes para exclusão, busca, etc., conforme necessário.
