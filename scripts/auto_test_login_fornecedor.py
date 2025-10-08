import os
import sys
# Ensure project root is on sys.path so local packages (data, routes, etc.) can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from utils.security import criar_hash_senha
from fastapi.testclient import TestClient
from main import app

# Config
email = "test_fornecedor@example.com"
password = "senha123456"
nome = "Fornecedor Teste"

def ensure_usuario(email, password, nome):
    user = usuario_repo.obter_usuario_por_email(email)
    senha_hash = criar_hash_senha(password)
    if user:
        # Atualiza senha
        usuario_repo.atualizar_senha_usuario(user.id, senha_hash)
        print(f"Atualizada senha do usuário existente id={user.id}")
        return usuario_repo.obter_usuario_por_email(email)
    else:
        usuario = Usuario(
            id=0,
            nome=nome,
            email=email,
            senha=senha_hash,
            cpf_cnpj="00000000000",
            telefone="",
            cep="",
            rua="",
            numero="",
            complemento="",
            bairro="",
            cidade="",
            estado="",
            data_cadastro=None,
            foto=None,
            token_redefinicao=None,
            data_token=None,
            tipo_usuario="Fornecedor"
        )
        new_id = usuario_repo.inserir_usuario(usuario)
        print(f"Inserido usuário fornecedor id={new_id}")
        return usuario_repo.obter_usuario_por_email(email)

if __name__ == '__main__':
    user = ensure_usuario(email, password, nome)

    client = TestClient(app)
    # Fazer login via AJAX headers
    resp = client.post('/login', data={'email': email, 'senha': password}, headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'})
    print('POST /login status:', resp.status_code)
    print('JSON response:', resp.text)
    print('Cookies after login:', resp.cookies)

    # agora acessar /fornecedor
    resp2 = client.get('/fornecedor')
    print('/fornecedor status:', resp2.status_code)
    if resp2.status_code == 200:
        print('Fornecedor page content sample:', resp2.text[:200])
    else:
        print('Fornecedor redirect or error, headers:', resp2.headers)
