import sqlite3

# Caminho pro seu banco
banco = "obratto.db"

conn = sqlite3.connect(banco)
cursor = conn.cursor()

# Adiciona a coluna estado, se não existir
cursor.execute("ALTER TABLE usuario ADD COLUMN estado TEXT NOT NULL DEFAULT ''")
cursor.execute("ALTER TABLE usuario ADD COLUMN cidade TEXT NOT NULL DEFAULT ''")
cursor.execute("ALTER TABLE usuario ADD COLUMN rua TEXT NOT NULL DEFAULT ''")
cursor.execute("ALTER TABLE usuario ADD COLUMN numero TEXT NOT NULL DEFAULT ''")
cursor.execute("ALTER TABLE usuario ADD COLUMN bairro TEXT NOT NULL DEFAULT ''")

conn.commit()
conn.close()
print("Coluna 'estado' adicionada com sucesso!")
print("Coluna 'cidade' adicionada com sucesso!")
print("Coluna 'rua' adicionada com sucesso!")
print("Coluna 'numero' adicionada com sucesso!")
print("Coluna 'bairro' adicionada com sucesso!")
