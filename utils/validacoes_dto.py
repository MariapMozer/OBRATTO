"""
Biblioteca centralizada de validações para DTOs
Contém funções reutilizáveis para validação de dados em formulários
"""

import re
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Any


class ValidacaoError(ValueError):
    """Exceção personalizada para erros de validação"""
    pass


def validar_cpf_cnpj(valor: Optional[str], campo: str = "CPF/CNPJ") -> Optional[str]:
    """
    Valida CPF ou CNPJ brasileiro com dígitos verificadores.

    Args:
        valor: Documento a ser validado (pode conter máscaras)
        campo: Nome do campo para mensagens de erro

    Returns:
        Documento limpo (apenas números) ou None se vazio

    Raises:
        ValidacaoError: Se o documento for inválido
    """
    if not valor:
        return None

    documento = re.sub(r'[^0-9]', '', valor)

    if len(documento) == 11:
        return validar_cpf_cnpj(documento)
    elif len(documento) == 14:
        return validar_cpf_cnpj(documento)
    else:
        raise ValidacaoError(f"{campo} deve conter 11 dígitos (CPF) ou 14 dígitos (CNPJ)")


def validar_telefone(telefone: str) -> str:
    if not telefone:
        raise ValidacaoError('Telefone é obrigatório')

    # Remover caracteres especiais
    telefone_limpo = re.sub(r'[^0-9]', '', telefone)

    if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
        raise ValidacaoError('Telefone deve ter 10 ou 11 dígitos')

    # Validar DDD
    ddd = telefone_limpo[:2]
    if not (11 <= int(ddd) <= 99):
        raise ValidacaoError('DDD inválido')

    return telefone_limpo


def validar_data_nascimento(data_str: Optional[str], idade_minima: int = 16) -> Optional[str]:
    """
    Valida data de nascimento

    Args:
        data_str: Data no formato YYYY-MM-DD
        idade_minima: Idade mínima permitida (padrão: 16 anos)

    Returns:
        Data validada ou None se vazia

    Raises:
        ValidacaoError: Se data for inválida
    """
    if not data_str:
        return None

    # Validar formato ISO (YYYY-MM-DD)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data_str):
        raise ValidacaoError('Data deve estar no formato YYYY-MM-DD')

    try:
        data_nasc = datetime.strptime(data_str, '%Y-%m-%d').date()
        hoje = date.today()

        if data_nasc > hoje:
            raise ValidacaoError('Data de nascimento não pode ser futura')

        # Verificar idade mínima
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        if idade < idade_minima:
            raise ValidacaoError(f'Idade mínima é {idade_minima} anos')

        # Verificar se não é uma idade absurda (mais de 120 anos)
        if idade > 120:
            raise ValidacaoError('Data de nascimento inválida')

    except ValueError as e:
        if "does not match format" in str(e):
            raise ValidacaoError('Data inválida')
        raise ValidacaoError(str(e))

    return data_str


def validar_nome_pessoa(nome: str, min_chars: int = 2, max_chars: int = 100) -> str:
    """
    Valida nome de pessoa (apenas letras, espaços e acentos)

    Args:
        nome: Nome a ser validado
        min_chars: Número mínimo de caracteres
        max_chars: Número máximo de caracteres

    Returns:
        Nome limpo (espaços extras removidos)

    Raises:
        ValidacaoError: Se nome for inválido
    """
    if not nome or not nome.strip():
        raise ValidacaoError('Nome é obrigatório')
    
    palavras = nome.split()
    if len(palavras) < 2:
        raise ValidacaoError(f'Nome deve ter pelo menos nome e sobrenome')
    
    nome_limpo = ''.join(nome.split())
    if len(nome_limpo) < min_chars:
        raise ValidacaoError(f'Nome deve ter pelo menos {min_chars} caracteres')
    
    if len(nome_limpo) > max_chars:
        raise ValidacaoError(f'Nome deve ter no máximo {max_chars} caracteres')


    # Verificar se contém apenas letras, espaços e acentos
    if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome_limpo):
        raise ValidacaoError('Nome deve conter apenas letras e espaços')

    return nome_limpo


def validar_texto_obrigatorio(texto: str, campo: str, min_chars: int = 1, max_chars: int = 1000) -> str:
    if not texto or not texto.strip():
        raise ValidacaoError(f'{campo} é obrigatório')

    # Remover espaços extras
    texto_limpo = ' '.join(texto.split())

    if len(texto_limpo) < min_chars:
        raise ValidacaoError(f'{campo} deve ter pelo menos {min_chars} caracteres')

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'{campo} deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_texto_opcional(texto: Optional[str], max_chars: int = 1000) -> Optional[str]:
    """
    Valida texto opcional com limite de caracteres

    Args:
        texto: Texto a ser validado
        max_chars: Número máximo de caracteres

    Returns:
        Texto limpo ou None se vazio

    Raises:
        ValidacaoError: Se texto exceder limite
    """
    if not texto:
        return None

    # Remover espaços extras
    texto_limpo = ' '.join(texto.split()) if texto.strip() else None

    if texto_limpo and len(texto_limpo) > max_chars:
        raise ValidacaoError(f'Texto deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_valor_monetario(valor: Any, campo: str = "Valor", obrigatorio: bool = True,
                          min_valor: Decimal = Decimal('0')) -> Optional[Decimal]:
    """
    Valida valor monetário

    Args:
        valor: Valor a ser validado
        campo: Nome do campo (para mensagens de erro)
        obrigatorio: Se o valor é obrigatório
        min_valor: Valor mínimo permitido

    Returns:
        Valor decimal validado ou None se opcional e vazio

    Raises:
        ValidacaoError: Se valor for inválido
    """
    if valor is None:
        if obrigatorio:
            raise ValidacaoError(f'{campo} é obrigatório')
        return None

    try:
        valor_decimal = Decimal(str(valor))
    except:
        raise ValidacaoError(f'{campo} deve ser um número válido')

    if valor_decimal < min_valor:
        if min_valor == 0:
            raise ValidacaoError(f'{campo} não pode ser negativo')
        else:
            raise ValidacaoError(f'{campo} deve ser maior ou igual a {min_valor}')

    # Verificar se tem no máximo 2 casas decimais
    if valor_decimal != round(valor_decimal, 2):
        raise ValidacaoError(f'{campo} deve ter no máximo 2 casas decimais')

    # Verificar se não é um valor absurdamente alto
    if valor_decimal > Decimal('9999999.99'):
        raise ValidacaoError(f'{campo} não pode ser superior a R$ 9.999.999,99')

    return valor_decimal


def validar_numero(numero: Any, campo: str = "Número", obrigatorio: bool = True,
                          min_valor: int = 0, max_valor: int = 9999) -> Optional[int]:
    """
    Valida número inteiro

    Args:
        numero: Número a ser validado
        campo: Nome do campo (para mensagens de erro)
        obrigatorio: Se o número é obrigatório
        min_valor: Valor mínimo permitido
        max_valor: Valor máximo permitido

    Returns:
        Número inteiro validado ou None se opcional e vazio

    Raises:
        ValidacaoError: Se número for inválido
    """
    if numero is None:
        if obrigatorio:
            raise ValidacaoError(f'{campo} é obrigatório')
        return None

    try:
        numero_int = int(numero)
    except:
        raise ValidacaoError(f'{campo} deve ser um número inteiro válido')

    if numero_int < min_valor:
        raise ValidacaoError(f'{campo} deve ser maior ou igual a {min_valor}')

    if numero_int > max_valor:
        raise ValidacaoError(f'{campo} deve ser menor ou igual a {max_valor}')

    return numero_int


def validar_estado_brasileiro(estado: Optional[str]) -> Optional[str]:
    """
    Valida sigla de estado brasileiro

    Args:
        estado: Sigla do estado (2 caracteres)

    Returns:
        Estado em maiúsculo ou None se vazio

    Raises:
        ValidacaoError: Se estado for inválido
    """
    if not estado:
        return None

    estado_upper = estado.strip().upper()

    if len(estado_upper) != 2:
        raise ValidacaoError('Estado deve ter exatamente 2 caracteres (sigla UF)')

    # Lista de estados brasileiros válidos
    estados_validos = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]

    if estado_upper not in estados_validos:
        raise ValidacaoError('Sigla de estado inválida')

    return estado_upper

def validar_cep(cep: Optional[str]) -> Optional[str]:
    """
    Valida CEP brasileiro

    Args:
        cep: CEP a ser validado (pode conter máscara)

    Returns:
        CEP limpo (apenas números) ou None se vazio

    Raises:
        ValidacaoError: Se CEP for inválido
    """
    if not cep:
        return None

    cep_limpo = re.sub(r'[^0-9]', '', cep)

    if len(cep_limpo) != 8:
        raise ValidacaoError('CEP deve conter exatamente 8 dígitos')

    return cep_limpo


def validar_senha(senha: Optional[str], min_chars: int = 6, max_chars: int = 128, obrigatorio: bool = True) -> Optional[str]:
    if not senha:
        if obrigatorio:
            raise ValidacaoError('Senha é obrigatória')
        return None

    if len(senha) < min_chars:
        raise ValidacaoError(f'Senha deve ter pelo menos {min_chars} caracteres')

    if len(senha) > max_chars:
        raise ValidacaoError(f'Senha deve ter no máximo {max_chars} caracteres')

    return senha


def validar_senhas_coincidem(senha: str, confirmar_senha: str) -> str:
    if senha != confirmar_senha:
        raise ValidacaoError('As senhas não coincidem')

    return confirmar_senha



def converter_checkbox_para_bool(valor: Any) -> bool:
    """
    Converte valor de checkbox HTML para boolean

    Args:
        valor: Valor do checkbox (pode ser 'on', True, False, etc.)

    Returns:
        Boolean correspondente
    """
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str):
        return valor.lower() in ['on', 'true', '1', 'yes']
    return bool(valor)


def validar_enum_valor(valor: Any, enum_class, campo: str = "Campo") -> Any:
    """
    Valida se valor está em um enum

    Args:
        valor: Valor a ser validado
        enum_class: Classe do enum
        campo: Nome do campo (para mensagens de erro)

    Returns:
        Valor do enum validado

    Raises:
        ValidacaoError: Se valor não estiver no enum
    """
    if isinstance(valor, str):
        try:
            return enum_class(valor.upper())
        except ValueError:
            valores_validos = [item.value for item in enum_class]
            raise ValidacaoError(f'{campo} deve ser uma das opções: {", ".join(valores_validos)}')

    if valor not in enum_class:
        valores_validos = [item.value for item in enum_class]
        raise ValidacaoError(f'{campo} deve ser uma das opções: {", ".join(valores_validos)}')

    return valor


# =====================================================
# WRAPPER PARA SIMPLIFICAR USO EM FIELD_VALIDATORS
# =====================================================

class ValidadorWrapper:
    """
    Classe para facilitar o uso de validadores em field_validators.
    Reduz código repetitivo e padroniza tratamento de erros.
    """

    @staticmethod
    def criar_validador(funcao_validacao, campo_nome: str = None, **kwargs):
        """
        Cria um validador pronto para usar com @field_validator.

        Args:
            funcao_validacao: Função de validação a ser chamada
            campo_nome: Nome do campo para mensagens de erro
            **kwargs: Argumentos adicionais para a função

        Returns:
            Função validador pronta para usar

        Exemplo:
            validar_nome = ValidadorWrapper.criar_validador(
                validar_nome_pessoa, "Nome", min_chars=2, max_chars=100
            )
        """
        def validador(valor):
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador

    @staticmethod
    def criar_validador_opcional(funcao_validacao, campo_nome: str = None, **kwargs):
        """
        Cria validador para campos opcionais.
        Retorna None se o valor for vazio, senão valida normalmente.

        Args:
            funcao_validacao: Função de validação a ser chamada
            campo_nome: Nome do campo para mensagens de erro
            **kwargs: Argumentos adicionais para a função

        Returns:
            Função validador para campos opcionais
        """
        def validador(valor):
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                return None
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador


# =====================================================
# VALIDADORES PRÉ-CONFIGURADOS COMUNS
# =====================================================

# Validadores mais usados, pré-configurados para facilitar uso
VALIDADOR_NOME = ValidadorWrapper.criar_validador(validar_nome_pessoa, "Nome")
VALIDADOR_EMAIL = ValidadorWrapper.criar_validador_opcional(lambda v, c: v, "Email")  # Pydantic já valida
VALIDADOR_SENHA = ValidadorWrapper.criar_validador(validar_senha, "Senha")
VALIDADOR_CPF_CNPJ = ValidadorWrapper.criar_validador(validar_cpf_cnpj, "CPF/CNPJ")
VALIDADOR_TELEFONE = ValidadorWrapper.criar_validador_opcional(validar_telefone, "Telefone")
VALIDADOR_CEP = ValidadorWrapper.criar_validador_opcional(lambda v, c: v, "CEP")  # Pode ser validado externamente
VALIDADOR_NUMERO = ValidadorWrapper.criar_validador_opcional(validar_numero, "Numero")
VALIDADOR_COMPLEMENTO = ValidadorWrapper.criar_validador_opcional(validar_texto_opcional, "Complemento", max_chars=100)
VALIDADOR_BAIRRO = ValidadorWrapper.criar_validador(validar_texto_obrigatorio, "Bairro", min_chars=2, max_chars=100)
VALIDADOR_CIDADE = ValidadorWrapper.criar_validador(validar_texto_obrigatorio, "Cidade", min_chars=2, max_chars=100)
VALIDADOR_ESTADO = ValidadorWrapper.criar_validador(validar_estado_brasileiro, "Estado")

