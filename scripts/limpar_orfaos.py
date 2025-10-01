import sqlite3
import os

def limpar_arquivos_orfaos():
    """Remove arquivos de imagem órfãos da pasta uploads"""
    
    # Obter o diretório do script e ir para o diretório pai
    script_dir = os.path.dirname(os.path.abspath(__file__))
    projeto_dir = os.path.dirname(script_dir)
    
    # Caminho para o banco de dados
    banco_path = os.path.join(projeto_dir, 'obratto.db')
    
    # Conectar ao banco e obter todos os caminhos de foto
    conn = sqlite3.connect(banco_path)
    cursor = conn.cursor()
    cursor.execute('SELECT foto FROM PRODUTO WHERE foto IS NOT NULL')
    fotos_banco = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    # Listar arquivos na pasta
    pasta_uploads = os.path.join(projeto_dir, "static", "uploads", "produtos_fornecedor")
    if not os.path.exists(pasta_uploads):
        print("Pasta uploads não encontrada")
        return
    
    arquivos_pasta = os.listdir(pasta_uploads)
    arquivos_removidos = 0
    
    for arquivo in arquivos_pasta:
        caminho_relativo = f"/static/uploads/produtos_fornecedor/{arquivo}"
        if caminho_relativo not in fotos_banco:
            caminho_completo = os.path.join(pasta_uploads, arquivo)
            try:
                os.remove(caminho_completo)
                print(f"Arquivo órfão removido: {arquivo}")
                arquivos_removidos += 1
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {e}")
    
    print(f"\nTotal de arquivos órfãos removidos: {arquivos_removidos}")

if __name__ == "__main__":
    print("Iniciando limpeza de arquivos órfãos...")
    limpar_arquivos_orfaos()
    print("Limpeza concluída!")