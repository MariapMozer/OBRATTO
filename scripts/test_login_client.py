from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Ajuste estes dados para um fornecedor existente na base de testes
email = "producencuba@gmail.com"
senha = "sua_senha_real_aqui"

response = client.post("/login", data={"email": email, "senha": senha}, headers={"X-Requested-With": "XMLHttpRequest"})
print("status_code:", response.status_code)
print("headers:")
for k, v in response.headers.items():
    print(k, ":", v)

try:
    print("json:", response.json())
except Exception as e:
    print("no json, text len:", len(response.text))

print("cookies:", response.cookies)

# Check session on client (TestClient stores cookies)
resp2 = client.get("/mensagens")
print("GET /mensagens status:", resp2.status_code)
print("GET /mensagens redirected?:", resp2.is_redirect)
print(resp2.text[:400])
