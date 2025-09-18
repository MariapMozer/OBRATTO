import os
from PIL import Image
from typing import List, Optional

# Funções destinadas ao Prestador 

def obter_diretorio_servico(servico_id: int) -> str:
    """Retorna o caminho do diretório de fotos de um servico"""
    codigo_servico = f"{servico_id:06d}"  # ← Formata com 6 dígitos (000001)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "static", "img", "servico", codigo_servico)


def obter_url_diretorio_servico(servico_id: int) -> str:
    """Retorna a URL do diretório de fotos de um servico"""
    codigo_servico = f"{servico_id:06d}"
    return f"/static/img/servico/{codigo_servico}"


def criar_diretorio_servico(servico_id: int) -> bool:
    """Cria o diretório de fotos do servico se não existir"""
    try:
        diretorio = obter_diretorio_servico(servico_id)
        os.makedirs(diretorio, exist_ok=True)
        return True
    except:
        return False


def processar_imagem(arquivo, caminho_destino: str) -> bool:
    """
    Processa uma imagem: corta para quadrado, redimensiona e salva como JPG
    """
    try:
        # 1. Abrir a imagem
        img = Image.open(arquivo)

        # 2. Converter para RGB se necessário (para salvar como JPG)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 3. Cortar para quadrado (centro da imagem)
        largura, altura = img.size
        tamanho = min(largura, altura)  # ← Usa o menor lado

        # Calcula coordenadas para corte centralizado
        left = (largura - tamanho) // 2
        top = (altura - tamanho) // 2
        right = left + tamanho
        bottom = top + tamanho

        img = img.crop((left, top, right, bottom))  # ← Corta para quadrado

        # 4. Redimensionar para tamanho padrão
        img = img.resize((800, 800), Image.Resampling.LANCZOS)

        # 5. Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        # 6. Salvar como JPG com qualidade otimizada
        img.save(caminho_destino, 'JPEG', quality=85, optimize=True)

        return True
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return False

def obter_foto_principal(servico_id: int) -> Optional[str]:
    """Retorna a URL da foto principal do produto ou None se não existir"""
    codigo_servico = f"{servico_id:06d}"
    caminho_foto = obter_diretorio_servico(servico_id) + f"/{codigo_servico}-001.jpg"

    if os.path.exists(caminho_foto):
        return f"/static/img/servico/{codigo_servico}/{codigo_servico}-001.jpg"
    return None

def obter_todas_fotos(servico_id: int) -> List[str]:
    """Retorna lista de URLs de todas as fotos do produto ordenadas"""
    codigo_servico = f"{servico_id:06d}"
    diretorio = obter_diretorio_servico(servico_id)

    if not os.path.exists(diretorio):
        return []

    fotos = []
    arquivos = os.listdir(diretorio)

    # Filtrar apenas arquivos JPG do produto
    for arquivo in arquivos:
        if arquivo.startswith(codigo_servico) and arquivo.endswith('.jpg'):
            fotos.append(f"/static/img/produservico/{codigo_servico}/{arquivo}")

    # Ordenar por número sequencial (001, 002, 003...)
    fotos.sort()
    return fotos

def obter_proximo_numero(servico_id: int) -> int:
    """Retorna o próximo número sequencial disponível para uma nova foto"""
    codigo_servico = f"{servico_id:06d}"
    diretorio = obter_diretorio_servico(servico_id)

    if not os.path.exists(diretorio):
        return 1

    numeros = []
    arquivos = os.listdir(diretorio)

    for arquivo in arquivos:
        if arquivo.startswith(codigo_servico) and arquivo.endswith('.jpg'):
            # Extrair número do arquivo (XXXXXX-NNN.jpg)
            try:
                numero_str = arquivo.split('-')[1].split('.')[0]
                numeros.append(int(numero_str))
            except:
                continue

    if not numeros:
        return 1

    return max(numeros) + 1  # ← Próximo número na sequência

def salvar_nova_foto(servico_id: int, arquivo, como_principal: bool = False) -> bool:
    """Salva uma nova foto do servico"""
    criar_diretorio_servico(servico_id)
    codigo_servico = f"{servico_id:06d}"

    if como_principal:
        # Salvar como foto principal (001)
        numero = 1
        # Se já existe foto principal, mover as outras para frente
        if obter_foto_principal(servico_id):
            _mover_fotos_para_frente(servico_id)
    else:
        # Adicionar como próxima foto na sequência
        numero = obter_proximo_numero(servico_id)

    # Gerar caminho do arquivo
    caminho_destino = f"{obter_diretorio_servico(servico_id)}/{codigo_servico}-{numero:03d}.jpg"
    return processar_imagem(arquivo, caminho_destino)

def excluir_foto(servico_id: int, numero: int) -> bool:
    """Remove uma foto específica e reordena as restantes"""
    codigo_servico = f"{servico_id:06d}"
    diretorio = obter_diretorio_servico(servico_id)

    # Remover o arquivo específico
    caminho_foto = f"{diretorio}/{codigo_servico}-{numero:03d}.jpg"

    if os.path.exists(caminho_foto):
        try:
            os.remove(caminho_foto)
        except:
            return False

    # Reordenar fotos restantes para não ter gaps na numeração
    return reordenar_fotos_automatico(servico_id)

def reordenar_fotos(servico_id: int, nova_ordem: List[int]) -> bool:
    """Reordena as fotos conforme a nova ordem especificada"""
    codigo_servico = f"{servico_id:06d}"
    diretorio = obter_diretorio_servico(servico_id)

    if not os.path.exists(diretorio):
        return False

    # Mapear arquivos existentes
    arquivos_existentes = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_servico) and arquivo.endswith('.jpg'):
            try:
                numero_str = arquivo.split('-')[1].split('.')[0]
                numero = int(numero_str)
                arquivos_existentes[numero] = arquivo
            except:
                continue

    # Validar nova ordem
    if len(nova_ordem) != len(arquivos_existentes):
        return False

    # Processo de renomeação em duas etapas para evitar conflitos:

    # Etapa 1: Renomear temporariamente
    temp_files = {}
    for i, numero_original in enumerate(nova_ordem):
        if numero_original not in arquivos_existentes:
            return False

        arquivo_original = arquivos_existentes[numero_original]
        caminho_original = f"{diretorio}/{arquivo_original}"
        caminho_temp = f"{diretorio}/temp_{i:03d}.jpg"

        try:
            os.rename(caminho_original, caminho_temp)
            temp_files[i] = caminho_temp
        except:
            return False

    # Etapa 2: Renomear para a sequência final
    for i in range(len(nova_ordem)):
        novo_numero = i + 1
        caminho_temp = temp_files[i]
        caminho_final = f"{diretorio}/{codigo_servico}-{novo_numero:03d}.jpg"

        try:
            os.rename(caminho_temp, caminho_final)
        except:
            return False

    return True


# Funções destinadas ao fornecedor