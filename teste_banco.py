import sqlite3
import os

banco = "obratto.db"  # coloque na mesma pasta do arquivo

# Verifica se o arquivo existe
if os.path.exists(banco):
    print("Arquivo do banco encontrado!")
else:
    print("Arquivo do banco NÃO encontrado!")

# Tenta abrir o banco
try:
    conn = sqlite3.connect(banco)
    print("Banco aberto com sucesso!")
    conn.close()
except Exception as e:
    print("Erro ao abrir o banco:", e)
