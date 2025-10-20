"""
Módulo de segurança para gerenciar senhas e tokens
"""
import secrets
import string
from datetime import datetime, timedelta
import bcrypt


def criar_hash_senha(senha: str) -> str:
    """
    Cria um hash seguro da senha usando bcrypt

    Args:
        senha: Senha em texto plano

    Returns:
        Hash da senha

    Note:
        Bcrypt tem limite de 72 bytes. Senhas mais longas são truncadas automaticamente.
    """
    # Bcrypt tem limite de 72 bytes - truncar se necessário
    senha_bytes = senha.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash

    Args:
        senha_plana: Senha em texto plano
        senha_hash: Hash da senha armazenado no banco

    Returns:
        True se a senha está correta, False caso contrário

    Note:
        Bcrypt tem limite de 72 bytes. Senhas mais longas são truncadas automaticamente.
    """
    try:
        # Bcrypt tem limite de 72 bytes - truncar se necessário (igual ao criar_hash_senha)
        senha_bytes = senha_plana.encode('utf-8')[:72]
        hash_bytes = senha_hash.encode('utf-8')
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except:
        return False


def gerar_token_redefinicao(tamanho: int = 32) -> str:
    """
    Gera um token aleatório seguro para redefinição de senha
    
    Args:
        tamanho: Tamanho do token em caracteres
    
    Returns:
        Token aleatório
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))


def obter_data_expiracao_token(horas: int = 24) -> str:
    """
    Calcula a data de expiração do token
    
    Args:
        horas: Número de horas de validade do token
    
    Returns:
        Data de expiração no formato ISO
    """
    expiracao = datetime.now() + timedelta(hours=horas)
    return expiracao.isoformat()


def validar_forca_senha(senha: str) -> tuple[bool, str]:
    """
    Valida se a senha atende aos requisitos FORTES de segurança

    Requisitos:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial (!@#$%^&*(),.?":{}|<>)

    Args:
        senha: Senha a ser validada

    Returns:
        Tupla (válida, mensagem de erro se inválida)
    """
    import re

    if not senha:
        return False, "Senha é obrigatória"

    if len(senha) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"

    if not re.search(r"[A-Z]", senha):
        return False, "Senha deve conter pelo menos uma letra maiúscula"

    if not re.search(r"[a-z]", senha):
        return False, "Senha deve conter pelo menos uma letra minúscula"

    if not re.search(r"\d", senha):
        return False, "Senha deve conter pelo menos um número"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False, "Senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>)"

    return True, ""


def gerar_senha_aleatoria(tamanho: int = 12) -> str:
    """
    Gera uma senha aleatória FORTE que atende todos os requisitos

    Args:
        tamanho: Tamanho da senha (mínimo 8, padrão 12)

    Returns:
        Senha aleatória que atende validar_forca_senha()
    """
    if tamanho < 8:
        tamanho = 8

    # Garantir que tem pelo menos um de cada tipo
    senha_lista = [
        secrets.choice(string.ascii_uppercase),  # Maiúscula
        secrets.choice(string.ascii_lowercase),  # Minúscula
        secrets.choice(string.digits),           # Número
        secrets.choice("!@#$%^&*(),.?\":{}|<>")  # Especial
    ]

    # Preencher o restante com caracteres aleatórios
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
    for _ in range(tamanho - 4):
        senha_lista.append(secrets.choice(caracteres))

    # Embaralhar para não ter padrão previsível
    secrets.SystemRandom().shuffle(senha_lista)

    return ''.join(senha_lista)


def calcular_nivel_senha(senha: str) -> str:
    """
    Calcula o nível de força da senha

    Args:
        senha: Senha a avaliar

    Returns:
        "fraca", "média" ou "forte"
    """
    import re

    pontos = 0

    if len(senha) >= 8: pontos += 1
    if len(senha) >= 12: pontos += 1
    if re.search(r"[A-Z]", senha): pontos += 1
    if re.search(r"[a-z]", senha): pontos += 1
    if re.search(r"\d", senha): pontos += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha): pontos += 1

    if pontos <= 2:
        return "fraca"
    elif pontos <= 4:
        return "média"
    else:
        return "forte"