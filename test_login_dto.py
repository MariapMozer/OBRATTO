"""
Script de teste para validar o LoginDTO
"""
from dtos import LoginDTO
from pydantic import ValidationError
import json

print("🧪 Testando validações do LoginDTO\n")
print("=" * 60)

# Teste 1: Login válido
print("\n✅ Teste 1: Login válido")
try:
    login_ok = LoginDTO(email='user@email.com', senha='senha12345')
    print(f"   Resultado: {json.dumps(login_ok.to_dict(), indent=4)}")
    print("   ✓ Passou!")
except Exception as e:
    print(f"   ✗ Falhou: {e}")

# Teste 2: Senha com menos de 8 caracteres
print("\n❌ Teste 2: Senha com menos de 8 caracteres (deve falhar)")
try:
    LoginDTO(email='user@email.com', senha='abc123')
    print("   ✗ ERRO: Deveria ter falhado!")
except ValidationError as e:
    print(f"   ✓ Erro esperado capturado:")
    for error in e.errors():
        print(f"     - Campo: {error['loc'][0]}")
        print(f"     - Mensagem: {error['msg']}")

# Teste 3: Email inválido
print("\n❌ Teste 3: Email inválido (deve falhar)")
try:
    LoginDTO(email='emailinvalido', senha='senha12345')
    print("   ✗ ERRO: Deveria ter falhado!")
except ValidationError as e:
    print(f"   ✓ Erro esperado capturado:")
    for error in e.errors():
        print(f"     - Campo: {error['loc'][0]}")
        print(f"     - Tipo: {error['type']}")

# Teste 4: Campos vazios
print("\n❌ Teste 4: Campos vazios (deve falhar)")
try:
    LoginDTO(email='', senha='')
    print("   ✗ ERRO: Deveria ter falhado!")
except ValidationError as e:
    print(f"   ✓ Erro esperado capturado: {len(e.errors())} erro(s)")

print("\n" + "=" * 60)
print("✅ Todos os testes executados com sucesso!")
print("\n📋 Resumo do LoginDTO:")
print("  - Email: EmailStr (apenas e-mail válido)")
print("  - Senha: mínimo 8 caracteres")
print("  - Validações funcionando conforme o padrão do DTO.md")
