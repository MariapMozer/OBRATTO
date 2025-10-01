import sqlite3

# Caminho pro seu banco
banco = "obratto.db"

conn = sqlite3.connect(banco)
cursor = conn.cursor()

try:
    # Adiciona a coluna foto, se não existir
    cursor.execute("ALTER TABLE PRODUTO ADD COLUMN foto TEXT")
    print("Coluna 'foto' adicionada com sucesso!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Coluna 'foto' já existe.")
    else:
        print(f"Erro ao adicionar coluna 'foto': {e}")

try:
    # Adiciona a coluna fornecedor_id, se não existir
    cursor.execute("ALTER TABLE PRODUTO ADD COLUMN fornecedor_id INTEGER")
    print("Coluna 'fornecedor_id' adicionada com sucesso!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Coluna 'fornecedor_id' já existe.")
    else:
        print(f"Erro ao adicionar coluna 'fornecedor_id': {e}")

conn.commit()
conn.close()
print("Atualização da tabela PRODUTO concluída!")