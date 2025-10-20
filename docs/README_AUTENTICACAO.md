# Sistema de Autenticação OBRATTO - Guia Rápido

## 🎯 O que foi implementado

✅ **Validação de senha FORTE** (8+ chars, maiúsc, minúsc, número, especial)  
✅ **Rate limiting** contra força bruta (configurável via .env)  
✅ **Logging profissional** com rotação de arquivos (logs/obratto.log)  
✅ **Recuperação de senha via email** (Resend.com)  
✅ **Enum centralizado de perfis** (`util/perfis.py`)  
✅ **Configuração via .env** (`.env.example` criado)  
✅ **Flash messages** melhorados  
✅ **Decorator de autenticação** com logs e validações robustas  

---

## 🚀 Início Rápido

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar .env

```bash
# Arquivo .env já foi criado com chave secreta gerada!
# Apenas adicione suas configurações de email (opcional):

# Para recuperação de senha via email:
RESEND_API_KEY=sua_chave_aqui  # https://resend.com/api-keys
RESEND_FROM_EMAIL=noreply@seudominio.com
```

### 3. Executar

```bash
python main.py
```

---

## 📋 Checklist de Uso

### Para Desenvolvedores

- [ ] **Usar Enum de Perfis** - Sempre importe `from util.perfis import Perfil`
- [ ] **Validar senhas fortes no cadastro** - Use `validar_forca_senha()`
- [ ] **Proteger rotas sensíveis** - Use `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] **Adicionar rate limiting** - Em login, cadastro, recuperação de senha
- [ ] **Logar eventos importantes** - `from utils.logger_config import logger`
- [ ] **Nunca commitar .env** - Adicione ao `.gitignore`

### Exemplos de Código

#### ✅ Proteger uma Rota

```python
from utils.auth_decorator import requer_autenticacao
from util.perfis import Perfil

@router.get("/admin")
@requer_autenticacao([Perfil.ADMINISTRADOR.value])
async def admin_page(request: Request, usuario_logado: dict):
    return {"usuario": usuario_logado}
```

#### ✅ Validar Senha Forte no Cadastro

```python
from utils.security import validar_forca_senha

# Em sua rota de cadastro
valida, mensagem = validar_forca_senha(senha)
if not valida:
    return {"erro": mensagem}
```

#### ✅ Usar Rate Limiting

```python
from utils.auth_decorator import SimpleRateLimiter
from util.config import RATE_LIMIT_LOGIN_MAX, RATE_LIMIT_LOGIN_MINUTOS

login_limiter = SimpleRateLimiter(RATE_LIMIT_LOGIN_MAX, RATE_LIMIT_LOGIN_MINUTOS)

@router.post("/login")
async def login(request: Request, ...):
    ip = request.client.host
    if not login_limiter.verificar(ip):
        return {"erro": "Muitas tentativas. Aguarde."}
    # ... processar login ...
```

#### ✅ Logar Eventos

```python
from utils.logger_config import logger

logger.info(f"Login bem-sucedido: {email}")
logger.warning(f"Tentativa de acesso não autorizado: {email}")
logger.error(f"Erro ao processar: {e}")
```

---

## 📊 Perfis Disponíveis

| Enum                         | Valor          | Descrição                |
|------------------------------|----------------|--------------------------|
| `Perfil.ADMINISTRADOR.value` | "Administrador"| Acesso total ao sistema |
| `Perfil.CLIENTE.value`       | "Cliente"      | Cliente do sistema      |
| `Perfil.FORNECEDOR.value`    | "Fornecedor"   | Fornecedor de produtos  |
| `Perfil.PRESTADOR.value`     | "Prestador"    | Prestador de serviços   |

**IMPORTANTE:** Sempre use o Enum, NUNCA strings literais!

```python
# ✅ Correto
from util.perfis import Perfil
if usuario.perfil == Perfil.ADMINISTRADOR.value:
    ...

# ❌ Errado
if usuario.perfil == "admin":  # NÃO FAZER!
    ...
```

---

## 🔐 Validação de Senha Forte

### Requisitos

- ✅ Mínimo **8 caracteres**
- ✅ Pelo menos **1 letra maiúscula** (A-Z)
- ✅ Pelo menos **1 letra minúscula** (a-z)
- ✅ Pelo menos **1 número** (0-9)
- ✅ Pelo menos **1 caractere especial** (`!@#$%^&*(),.?":{}|<>`)

### Exemplos de Senhas

| Senha           | Válida? | Motivo                                |
|-----------------|---------|---------------------------------------|
| `12345678`      | ❌       | Faltam letras e caractere especial   |
| `senha123`      | ❌       | Faltam maiúscula e especial          |
| `Senha123`      | ❌       | Falta caractere especial             |
| `Senha@123`     | ✅       | Atende todos os requisitos           |
| `Admin@2025`    | ✅       | Atende todos os requisitos           |

---

## 🛡️ Rate Limiting (Proteção contra Força Bruta)

### Configuração Padrão (via .env)

```env
# Login
RATE_LIMIT_LOGIN_MAX=5           # 5 tentativas
RATE_LIMIT_LOGIN_MINUTOS=5       # Em 5 minutos

# Cadastro
RATE_LIMIT_CADASTRO_MAX=3        # 3 tentativas
RATE_LIMIT_CADASTRO_MINUTOS=10   # Em 10 minutos

# Recuperação de Senha
RATE_LIMIT_ESQUECI_SENHA_MAX=1    # 1 tentativa
RATE_LIMIT_ESQUECI_SENHA_MINUTOS=1  # Por minuto
```

### Como Funciona

- Bloqueia tentativas excessivas **por IP**
- Janela deslizante (limpa tentativas antigas automaticamente)
- Logs de bloqueios em `logs/obratto.log`

---

## 📧 Recuperação de Senha via Email

### 1. Configurar Resend.com

1. Criar conta em [resend.com](https://resend.com)
2. Obter API Key
3. Adicionar ao `.env`:

```env
RESEND_API_KEY=re_abc123...
RESEND_FROM_EMAIL=noreply@seudominio.com
```

### 2. Usar o EmailService

```python
from utils.email_service import email_service

# Recuperação de senha
email_service.enviar_recuperacao_senha(
    para_email=usuario.email,
    para_nome=usuario.nome,
    token=token_gerado
)

# Boas-vindas
email_service.enviar_boas_vindas(
    para_email=usuario.email,
    para_nome=usuario.nome,
    perfil=usuario.perfil
)
```

---

## 📝 Logging

### Níveis de Log

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Arquivos de Log

- **Localização**: `logs/obratto.log`
- **Rotação**: Automática (10MB por arquivo, 10 backups)
- **Também no console**: Para desenvolvimento

### Verificar Logs

```bash
# Ver logs em tempo real
tail -f logs/obratto.log

# Buscar erros
cat logs/obratto.log | grep -i error

# Buscar tentativas de login
cat logs/obratto.log | grep -i login
```

---

## ⚠️ Troubleshooting

| Problema                           | Solução                                |
|------------------------------------|----------------------------------------|
| `ModuleNotFoundError: dotenv`      | `pip install python-dotenv`           |
| `ModuleNotFoundError: resend`      | `pip install resend`                  |
| Email não envia                    | Verificar `RESEND_API_KEY` no .env    |
| Rate limit não funciona            | Verificar se .env está carregado      |
| Logs não aparecem                  | Verificar permissões do diretório logs/|
| Senha fraca aceita                 | Usar `validar_forca_senha()` no cadastro |

---

## 📚 Documentação Completa

Para detalhes completos, consulte:

📖 **[docs/SISTEMA_AUTENTICACAO.md](./SISTEMA_AUTENTICACAO.md)**

---

## ✅ Próximos Passos (Opcionais)

- [ ] Implementar 2FA (TOTP)
- [ ] OAuth (Google, GitHub)
- [ ] Confirmação de email
- [ ] Bloqueio de conta após N tentativas
- [ ] Auditoria de login (tabela de logs)
- [ ] Sessões persistentes ("Lembrar-me")

---

**Versão:** 1.0.0  
**Data:** Janeiro 2025  
**Status:** ✅ Pronto para uso
