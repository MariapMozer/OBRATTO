import sys
sys.path.insert(0, '.')

from util.security import criar_hash_senha
from util.db import open_connection

# Senha padrão
senha_padrao = "Senha@123"
novo_hash = criar_hash_senha(senha_padrao)

print(f"🔑 Criando novo hash para senha: {senha_padrao}")
print(f"   Novo hash: {novo_hash[:50]}...")

# Atualizar todos os usuários
with open_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE usuario SET senha = ?", (novo_hash,))
    conn.commit()
    print(f"\n✅ {cursor.rowcount} senhas atualizadas no banco!")
    
print(f"\n🎯 Agora todos os usuários podem logar com: {senha_padrao}")
