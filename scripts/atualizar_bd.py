import sqlite3
import os

# Obter o diretório do script e ir para o diretório pai
script_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.dirname(script_dir)

# Caminho para o banco de dados
banco = os.path.join(projeto_dir, "obratto.db")

conn = sqlite3.connect(banco)
cursor = conn.cursor()

# Lista de colunas para adicionar
colunas = [
    ("estado", "TEXT NOT NULL DEFAULT ''"),
    ("cidade", "TEXT NOT NULL DEFAULT ''"),
    ("rua", "TEXT NOT NULL DEFAULT ''"),
    ("numero", "TEXT NOT NULL DEFAULT ''"),
    ("bairro", "TEXT NOT NULL DEFAULT ''")
]

for nome_coluna, tipo_coluna in colunas:
    try:
        cursor.execute(f"ALTER TABLE usuario ADD COLUMN {nome_coluna} {tipo_coluna}")
        print(f"Coluna '{nome_coluna}' adicionada com sucesso!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"Coluna '{nome_coluna}' já existe.")
        else:
            print(f"Erro ao adicionar coluna '{nome_coluna}': {e}")

conn.commit()
conn.close()
print("Atualização da tabela usuario concluída!")
