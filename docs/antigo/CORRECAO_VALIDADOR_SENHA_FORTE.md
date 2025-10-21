# Correção: Função validar_senha_forte

## ❌ Problema

Os testes do pytest não conseguiam ser descobertos devido ao erro:

```
NameError: name 'validar_senha_forte' is not defined
```

**Arquivo afetado:** `utils/validacoes_dto.py` (linha 522)

**Causa:** A função `validar_senha_forte` estava sendo referenciada para criar o validador pré-configurado `VALIDADOR_SENHA_FORTE`, mas a função não existia no arquivo.

## ✅ Solução

Criei a função `validar_senha_forte()` em `utils/validacoes_dto.py` com os seguintes requisitos de segurança:

### Requisitos da Senha Forte

- ✅ **Mínimo 8 caracteres** (configurável)
- ✅ **Pelo menos uma letra maiúscula** (A-Z)
- ✅ **Pelo menos uma letra minúscula** (a-z)
- ✅ **Pelo menos um número** (0-9)
- ✅ **Pelo menos um caractere especial** (!@#$%^&*...)

### Implementação

```python
def validar_senha_forte(senha: Optional[str], min_chars: int = 8, max_chars: int = 128,
                        obrigatorio: bool = True) -> Optional[str]:
    """
    Valida senha forte com requisitos de segurança:
    - Mínimo 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial

    Args:
        senha: Senha a ser validada
        min_chars: Número mínimo de caracteres (padrão: 8)
        max_chars: Número máximo de caracteres
        obrigatorio: Se a senha é obrigatória

    Returns:
        Senha validada ou None se opcional e vazia

    Raises:
        ValidacaoError: Se senha não atender aos requisitos
    """
    import re

    if not senha:
        if obrigatorio:
            raise ValidacaoError('Senha é obrigatória')
        return None

    if len(senha) < min_chars:
        raise ValidacaoError(f'Senha deve ter pelo menos {min_chars} caracteres')

    if len(senha) > max_chars:
        raise ValidacaoError(f'Senha deve ter no máximo {max_chars} caracteres')

    # Verificar letra maiúscula
    if not re.search(r'[A-Z]', senha):
        raise ValidacaoError('Senha deve conter pelo menos uma letra maiúscula')

    # Verificar letra minúscula
    if not re.search(r'[a-z]', senha):
        raise ValidacaoError('Senha deve conter pelo menos uma letra minúscula')

    # Verificar número
    if not re.search(r'[0-9]', senha):
        raise ValidacaoError('Senha deve conter pelo menos um número')

    # Verificar caractere especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/`~]', senha):
        raise ValidacaoError('Senha deve conter pelo menos um caractere especial (!@#$%^&*...)')

    return senha
```

## 🧪 Testes

### Testes Automatizados

Todos os casos foram testados com sucesso:

- ✅ **Senha forte válida:** `Senha@123` → Aceita
- ✅ **Sem maiúscula:** `senha@123` → Rejeitada
- ✅ **Sem minúscula:** `SENHA@123` → Rejeitada
- ✅ **Sem número:** `Senha@Abc` → Rejeitada
- ✅ **Sem caractere especial:** `Senha123` → Rejeitada
- ✅ **Muito curta:** `Ab@1` → Rejeitada

### Resultado da Descoberta de Testes

**Antes:**
```
ERROR - NameError: name 'validar_senha_forte' is not defined
Interrupted: 3 errors during collection
```

**Depois:**
```
✅ 122 tests collected in 0.59s
```

## 📝 Como Usar

### No Backend (DTOs)

O validador pré-configurado `VALIDADOR_SENHA_FORTE` já está disponível:

```python
from utils.validacoes_dto import VALIDADOR_SENHA_FORTE
from pydantic import BaseModel, field_validator

class CadastroUsuarioDTO(BaseModel):
    email: str
    senha: str

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v):
        return VALIDADOR_SENHA_FORTE(v)
```

### Uso Direto

```python
from utils.validacoes_dto import validar_senha_forte, ValidacaoError

try:
    senha_validada = validar_senha_forte("Senha@123")
    print("Senha válida!")
except ValidacaoError as e:
    print(f"Erro: {e}")
```

### Personalizar Requisitos

```python
# Senha forte com mínimo 10 caracteres
senha = validar_senha_forte("SenhaForte@123", min_chars=10)

# Senha forte opcional
senha = validar_senha_forte(None, obrigatorio=False)  # Retorna None
```

## 🔒 Segurança

Esta implementação segue as melhores práticas de validação de senha:

1. **OWASP Guidelines:** Atende aos requisitos de complexidade
2. **NIST SP 800-63B:** Comprimento mínimo de 8 caracteres
3. **Mensagens claras:** Feedback específico sobre o que está faltando
4. **Caracteres especiais:** Lista ampla de caracteres aceitos

## ⚠️ Diferença entre Validadores

O projeto agora possui dois validadores de senha:

### `validar_senha()` - Básico
- Apenas valida comprimento (6-128 caracteres)
- Sem requisitos de complexidade
- Usado para login e operações simples
- **Uso:** `VALIDADOR_SENHA`

### `validar_senha_forte()` - Forte
- Valida comprimento (8-128 caracteres)
- Requer maiúscula, minúscula, número e especial
- Usado para cadastro e troca de senha
- **Uso:** `VALIDADOR_SENHA_FORTE`

## 📍 Localização

**Arquivo:** `/Volumes/Externo/Ifes/PI/OBRATTO/utils/validacoes_dto.py`
**Linhas:** 383-434

---

**Status:** ✅ Problema resolvido e testado
**Data:** 2025-10-20
