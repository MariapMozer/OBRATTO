import sqlite3
import os


def open_connection():
    """Abre conexão com o banco de dados obratto.db, garantindo fechamento correto."""
    database_path = os.environ.get('TEST_DATABASE_PATH', 'obratto.db')
    conexao = sqlite3.connect(database_path, check_same_thread=False)
    conexao.row_factory = sqlite3.Row
    return conexao

def get_database_info():
    """Retorna informações sobre o banco de dados"""
    try:
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            return {
                'database_file': 'obratto.db',
                'tables': tables,
                'status': 'connected'
            }
    except Exception as e:
        return {
            'database_file': 'obratto.db',
            'tables': [],
            'status': f'error: {str(e)}'
        }