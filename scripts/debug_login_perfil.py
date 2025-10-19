import sys
import os
# Garantir que o diretório do projeto esteja no path para importar main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from main import app
from data.usuario import usuario_repo
from utils.security import criar_hash_senha

client = TestClient(app)

# Ensure test fornecedor exists (email abaixo deve coincidir com um do DB ou crie um novo)
email = "fornecedor_teste@example.com"
senha = "senha123"

user = usuario_repo.obter_usuario_por_email(email)
if not user:
    from data.fornecedor.fornecedor_model import Fornecedor
    f = Fornecedor(
        id=0,
        nome="Fornecedor Teste",
        email=email,
        senha=criar_hash_senha(senha),
        cpf_cnpj="00000000000",
        telefone="000000000",
        cep="",
        estado="",
        cidade="",
        rua="",
        numero="",
        complemento="",
        bairro="",
        data_cadastro=None,
        razao_social="Fornecedor Teste",
        selo_confianca=False,
        tipo_usuario="Fornecedor"
    )
    from data.fornecedor import fornecedor_repo
    novo_id = fornecedor_repo.inserir_fornecedor(f)
    print("Inserido fornecedor teste id:", novo_id)
else:
    print("Fornecedor já existe id:", user.id)

# Após garantir existência do usuário, certificar que há um registro na tabela fornecedor
from data.fornecedor import fornecedor_repo
forn = fornecedor_repo.obter_fornecedor_por_id(user.id if user else novo_id)
if not forn:
    import sqlite3
    from utils.db import open_connection
    uid = user.id if user else novo_id
    with open_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT OR IGNORE INTO fornecedor (id, razao_social, selo_confianca) VALUES (?, ?, ?)", (uid, 'Fornecedor Teste', 0))
            conn.commit()
            print('Inserido registro em fornecedor para id', uid)
        except Exception as e:
            print('Erro ao inserir fornecedor:', e)
else:
    print('Registro fornecedor já presente para id', forn.id)

# Faz login
resp = client.post("/login", data={"email": email, "senha": senha})
print("POST /login status:", resp.status_code)
print("Location header:", resp.headers.get('location'))
print("Cookies:", resp.cookies)

# Follow redirect (if any) or access perfil directly
if resp.status_code in (302, 303) and resp.headers.get('location'):
    loc = resp.headers.get('location')
    r2 = client.get(loc)
    print(loc, "status:", r2.status_code)
    print(r2.text[:500])
else:
    r3 = client.get("/fornecedor/perfil")
    print("GET /fornecedor/perfil status:", r3.status_code)
    print(r3.text[:500])
