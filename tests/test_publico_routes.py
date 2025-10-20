import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_form():
    response = client.get("/publico/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

def test_cadastrar_usuario_cliente():
    response = client.post("/publico/cadastrar_usuario", data={
        "tipo_usuario": "cliente",
        "nome": "Teste Cliente",
        "email": "cliente@teste.com",
        "senha": "123456",
        "cpf_cnpj": "12345678900",
        "telefone": "11999999999",
        "endereco": "Rua Teste",
        "genero": "M",
        "data_nascimento": "2000-01-01"
    })
    assert response.status_code == 200
    assert "Cadastro Sucesso" in response.text

def test_cadastrar_usuario_fornecedor():
    response = client.post("/publico/cadastrar_usuario", data={
        "tipo_usuario": "fornecedor",
        "nome": "Teste Fornecedor",
        "email": "fornecedor@teste.com",
        "senha": "123456",
        "cpf_cnpj": "12345678901",
        "telefone": "11988888888",
        "endereco": "Rua Fornecedor",
        "razao_social": "Fornecedor Teste"
    })
    assert response.status_code == 200
    assert "Cadastro Sucesso" in response.text

def test_cadastrar_usuario_prestador():
    response = client.post("/publico/cadastrar_usuario", data={
        "tipo_usuario": "prestador",
        "nome": "Teste Prestador",
        "email": "prestador@teste.com",
        "senha": "123456",
        "cpf_cnpj": "12345678902",
        "telefone": "11977777777",
        "endereco": "Rua Prestador",
        "area_atuacao": "TI",
        "tipo_pessoa": "Física",
        "razao_social": "Prestador Teste",
        "descricao_servicos": "Serviços de TI"
    })
    assert response.status_code == 200
    assert "Cadastro Sucesso" in response.text

def test_cadastrar_usuario_admin():
    response = client.post("/publico/cadastrar_usuario", data={
        "tipo_usuario": "admin",
        "nome": "Teste Admin",
        "email": "admin@teste.com",
        "senha": "123456",
        "cpf_cnpj": "12345678900",
        "telefone": "11999999999",
        "endereco": "Rua Teste, 123"
    })
    assert response.status_code == 200
    assert "Cadastro Sucesso" in response.text

def test_alterar_senha_usuario():
    # Supondo que o id 1 existe
    response = client.post("/publico/perfil/alterar_senha/1", data={"senha_nova": "nova_senha"})
    assert response.status_code == 200
    assert "Senha alterada com sucesso" in response.text

def test_ver_mensagens():
    # Supondo que o id 1 existe
    response = client.get("/publico/mensagens/1")
    assert response.status_code == 200
    assert "mensagens" in response.text.lower()

def test_enviar_mensagem():
    response = client.post("/publico/mensagens/enviar", data={
        "id_remetente": "1",
        "id_destinatario": "2",
        "conteudo": "Olá!",
        "nome_remetente": "Remetente",
        "nome_destinatario": "Destinatário"
    })
    assert response.status_code == 200
    assert "Mensagem enviada com sucesso" in response.text

def test_responder_mensagem():
    # Supondo que o id 1 existe
    response = client.post("/publico/mensagens/responder/1", data={
        "resposta": "Resposta!",
        "nome_remetente": "Destinatário",
        "nome_destinatario": "Remetente"
    })
    assert response.status_code == 200
    assert "Resposta enviada com sucesso" in response.text
