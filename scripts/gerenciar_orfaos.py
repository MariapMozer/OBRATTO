import sqlite3
import os
import argparse

def obter_caminhos_projeto():
    """Obtém os caminhos do projeto"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    projeto_dir = os.path.dirname(script_dir)
    banco_path = os.path.join(projeto_dir, 'obratto.db')
    pasta_uploads = os.path.join(projeto_dir, "static", "uploads", "produtos_fornecedor")
    return projeto_dir, banco_path, pasta_uploads

def obter_fotos_banco(banco_path):
    """Obtém lista de fotos referenciadas no banco de dados"""
    conn = sqlite3.connect(banco_path)
    cursor = conn.cursor()
    cursor.execute('SELECT foto FROM PRODUTO WHERE foto IS NOT NULL')
    fotos_banco = [row[0] for row in cursor.fetchall()]
    conn.close()
    return fotos_banco

def verificar_arquivos_orfaos():
    """Verifica se há arquivos de imagem órfãos na pasta uploads"""
    projeto_dir, banco_path, pasta_uploads = obter_caminhos_projeto()
    
    print("🔍 Verificando arquivos órfãos...")
    print("-" * 50)
    
    # Obter fotos do banco
    fotos_banco = obter_fotos_banco(banco_path)
    
    print(f"📊 Fotos no banco: {len(fotos_banco)}")
    for foto in fotos_banco:
        print(f"  - {foto}")
    
    # Listar arquivos na pasta
    if os.path.exists(pasta_uploads):
        arquivos_pasta = os.listdir(pasta_uploads)
        print(f"\n📁 Arquivos na pasta: {len(arquivos_pasta)}")
        for arquivo in arquivos_pasta:
            print(f"  - {arquivo}")
        
        # Verificar arquivos órfãos
        arquivos_orfaos = []
        for arquivo in arquivos_pasta:
            caminho_relativo = f"/static/uploads/produtos_fornecedor/{arquivo}"
            if caminho_relativo not in fotos_banco:
                arquivos_orfaos.append(arquivo)
        
        print(f"\n🗑️  Arquivos órfãos encontrados: {len(arquivos_orfaos)}")
        if arquivos_orfaos:
            for orfao in arquivos_orfaos:
                print(f"  - {orfao}")
            
            # Calcular tamanho dos arquivos órfãos
            tamanho_total = 0
            for orfao in arquivos_orfaos:
                caminho_completo = os.path.join(pasta_uploads, orfao)
                if os.path.exists(caminho_completo):
                    tamanho_total += os.path.getsize(caminho_completo)
            
            print(f"\n💾 Espaço ocupado por órfãos: {tamanho_total / 1024:.2f} KB")
        else:
            print("  ✅ Nenhum arquivo órfão encontrado!")
        
        return arquivos_orfaos
    else:
        print("❌ Pasta uploads não encontrada")
        return []

def limpar_arquivos_orfaos(confirmar=True):
    """Remove arquivos de imagem órfãos da pasta uploads"""
    projeto_dir, banco_path, pasta_uploads = obter_caminhos_projeto()
    
    print("🧹 Iniciando limpeza de arquivos órfãos...")
    print("-" * 50)
    
    # Obter fotos do banco
    fotos_banco = obter_fotos_banco(banco_path)
    
    # Listar arquivos na pasta
    if not os.path.exists(pasta_uploads):
        print("❌ Pasta uploads não encontrada")
        return
    
    arquivos_pasta = os.listdir(pasta_uploads)
    arquivos_orfaos = []
    
    for arquivo in arquivos_pasta:
        caminho_relativo = f"/static/uploads/produtos_fornecedor/{arquivo}"
        if caminho_relativo not in fotos_banco:
            arquivos_orfaos.append(arquivo)
    
    if not arquivos_orfaos:
        print("✅ Nenhum arquivo órfão encontrado!")
        return
    
    print(f"🗑️  Encontrados {len(arquivos_orfaos)} arquivos órfãos:")
    tamanho_total = 0
    for orfao in arquivos_orfaos:
        caminho_completo = os.path.join(pasta_uploads, orfao)
        if os.path.exists(caminho_completo):
            tamanho = os.path.getsize(caminho_completo)
            tamanho_total += tamanho
            print(f"  - {orfao} ({tamanho / 1024:.2f} KB)")
    
    print(f"\n💾 Total a ser liberado: {tamanho_total / 1024:.2f} KB")
    
    if confirmar:
        resposta = input("\n⚠️  Deseja remover estes arquivos? (s/N): ").strip().lower()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            print("❌ Operação cancelada pelo usuário")
            return
    
    # Remover arquivos
    arquivos_removidos = 0
    for arquivo in arquivos_orfaos:
        caminho_completo = os.path.join(pasta_uploads, arquivo)
        try:
            os.remove(caminho_completo)
            print(f"✅ Removido: {arquivo}")
            arquivos_removidos += 1
        except Exception as e:
            print(f"❌ Erro ao remover {arquivo}: {e}")
    
    print(f"\n🎉 Limpeza concluída! {arquivos_removidos} arquivos removidos")

def main():
    parser = argparse.ArgumentParser(description='Gerenciar arquivos órfãos de imagens')
    parser.add_argument('acao', choices=['verificar', 'limpar'], 
                       help='Ação a executar: verificar ou limpar arquivos órfãos')
    parser.add_argument('--force', action='store_true', 
                       help='Limpar sem confirmação (apenas para ação limpar)')
    
    args = parser.parse_args()
    
    if args.acao == 'verificar':
        verificar_arquivos_orfaos()
    elif args.acao == 'limpar':
        limpar_arquivos_orfaos(confirmar=not args.force)

if __name__ == "__main__":
    import sys
    # Se executado sem argumentos, executa no modo interativo
    if len(sys.argv) == 1:
        print("🖼️  Gerenciador de Arquivos Órfãos - OBRATTO")
        print("=" * 50)
        print("1. Verificar arquivos órfãos")
        print("2. Limpar arquivos órfãos")
        print("0. Sair")
        
        while True:
            try:
                opcao = input("\nEscolha uma opção (0-2): ").strip()
                
                if opcao == '0':
                    print("👋 Até logo!")
                    break
                elif opcao == '1':
                    print()
                    verificar_arquivos_orfaos()
                elif opcao == '2':
                    print()
                    limpar_arquivos_orfaos()
                else:
                    print("❌ Opção inválida! Tente novamente.")
                    
                input("\nPressione Enter para continuar...")
                print("\n" + "=" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Operação cancelada. Até logo!")
                break
    else:
        main()