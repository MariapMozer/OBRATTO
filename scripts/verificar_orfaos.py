import sqlite3
import os

def verificar_arquivos_orfaos():
    """Verifica se há arquivos de imagem órfãos na pasta uploads"""
    
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
    
    print(f"Fotos no banco: {len(fotos_banco)}")
    for foto in fotos_banco:
        print(f"  - {foto}")
    
    # Listar arquivos na pasta
    pasta_uploads = os.path.join(projeto_dir, "static", "uploads", "produtos_fornecedor")
    if os.path.exists(pasta_uploads):
        arquivos_pasta = os.listdir(pasta_uploads)
        print(f"\nArquivos na pasta: {len(arquivos_pasta)}")
        for arquivo in arquivos_pasta:
            print(f"  - {arquivo}")
        
        # Verificar arquivos órfãos
        arquivos_orfaos = []
        for arquivo in arquivos_pasta:
            caminho_relativo = f"/static/uploads/produtos_fornecedor/{arquivo}"
            if caminho_relativo not in fotos_banco:
                arquivos_orfaos.append(arquivo)
        
        print(f"\nArquivos órfãos encontrados: {len(arquivos_orfaos)}")
        for orfao in arquivos_orfaos:
            print(f"  - {orfao}")
    else:
        print("Pasta uploads não encontrada")

if __name__ == "__main__":
    verificar_arquivos_orfaos()