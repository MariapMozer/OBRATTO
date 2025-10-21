# Sistema de Autenticação/Autorização OBRATTO

## Visão Geral

O sistema de autenticação do OBRATTO foi aprimorado com as seguintes funcionalidades:

### ✅ Recursos Implementados

1. **Autenticação baseada em sessão** (SessionMiddleware)
2. **Validação de senha FORTE** (8+ chars, maiúsc, minúsc, número, especial)
3. **Rate limiting** para proteção contra força bruta
4. **Logging profissional** com rotação de arquivos
5. **Recuperação de senha via email** (Resend.com)
6. **Flash messages** para feedback ao usuário
7. **Enum centralizado de perfis** para consistência
8. **Configuração via .env** para facilitar deploy

---

## Estrutura de Arquivos

### Novos Arquivos Criados

```
OBRATTO/
├── .env                         # Configurações (NÃO commitar!)
├── .env.example                 # Template de configuração
├── util/
│   ├── __init__.py
│   ├── config.py               # Configurações centralizadas
│   └── perfis.py               # Enum de perfis (fonte da verdade)
├── utils/
│   ├── security.py             # Validações de senha FORTE
│   ├── logger_config.py        # Logging profissional
│   ├── email_service.py        # Serviço de email (Resend.com)
│   └── auth_decorator.py       # Melhorado com rate limit e logs
└── logs/
    └── obratto.log             # Logs da aplicação (rotativo, 10MB)
```

### Arquivos Modificados

- `requirements.txt` - Adicionado `python-dotenv` e `resend`
- `main.py` - Integração com configurações do .env
- `utils/validacoes_dto.py` - Adicionado validador de senha forte
- `dtos/usuario/login_dto.py` - Melhorado validação

---

## Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar .env

O arquivo `.env.example` foi criado como template. Copie e ajuste:

```bash
cp .env.example .env
```

**Configurações importantes:**

```env
# Aplicação
APP_NAME=OBRATTO
SECRET_KEY=FWK3R-ZHPxJKnisqBJcmvYHJA5f2bACgrAzsjL_LWvY  # JÁ GERADA!

# Email (Opcional - para recuperação de senha)
RESEND_API_KEY=                    # Obtenha em: https://resend.com/api-keys
RESEND_FROM_EMAIL=noreply@seudominio.com
RESEND_FROM_NAME=OBRATTO

# Rate Limiting (Proteção)
RATE_LIMIT_LOGIN_MAX=5             # 5 tentativas de login
RATE_LIMIT_LOGIN_MINUTOS=5         # Em 5 minutos
RATE_LIMIT_CADASTRO_MAX=3          # 3 tentativas de cadastro
RATE_LIMIT_CADASTRO_MINUTOS=10     # Em 10 minutos
```

### 3. Executar a Aplicação

```bash
python main.py
```

Ou com uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Perfis de Usuário

### Enum Centralizado (util/perfis.py)

**IMPORTANTE:** Sempre use o Enum `Perfil`, NUNCA strings literais!

```python
from util.perfis import Perfil

# ✅ Correto
perfis_permitidos = [Perfil.ADMINISTRADOR.value]

# ❌ Errado (não use!)
perfis_permitidos = ["admin"]  # NÃO FAZER ISSO!
```

### Perfis Disponíveis

- `Perfil.ADMINISTRADOR` → "Administrador"
- `Perfil.CLIENTE` → "Cliente"
- `Perfil.FORNECEDOR` → "Fornecedor"
- `Perfil.PRESTADOR` → "Prestador"

### Métodos Úteis

```python
# Verificar se perfil existe
Perfil.existe("Cliente")  # True

# Converter string para Enum (case-insensitive)
perfil = Perfil.from_string("admin")  # Perfil.ADMINISTRADOR

# Validar perfil (levanta exceção se inválido)
perfil = Perfil.validar("Cliente")  # "Cliente"

# Listar todos os perfis
perfis = Perfil.valores()  # ["Administrador", "Cliente", "Fornecedor", "Prestador"]

# Perfis que podem se auto-cadastrar
perfis_publicos = Perfil.perfis_cadastro_publico()  # ["Cliente", "Fornecedor", "Prestador"]
```

---

## Proteção de Rotas

### Decorator `@requer_autenticacao()`

```python
from fastapi import APIRouter, Request
from utils.auth_decorator import requer_autenticacao
from util.perfis import Perfil

router = APIRouter()

# Rota pública (sem decorator)
@router.get("/")
async def home(request: Request):
    return {"message": "Público"}

# Rota protegida (qualquer usuário logado)
@router.get("/perfil")
@requer_autenticacao()
async def perfil(request: Request, usuario_logado: dict):
    # usuario_logado é injetado automaticamente
    return {"usuario": usuario_logado}

# Rota protegida (apenas Administrador)
@router.get("/admin")
@requer_autenticacao([Perfil.ADMINISTRADOR.value])
async def admin_page(request: Request, usuario_logado: dict):
    return {"admin": True}

# Rota protegida (múltiplos perfis)
@router.get("/dashboard")
@requer_autenticacao([Perfil.ADMINISTRADOR.value, Perfil.FORNECEDOR.value])
async def dashboard(request: Request, usuario_logado: dict):
    return {"dashboard": usuario_logado}
```

### Funcionalidades do Decorator

- ✅ **Autentic validar**: Redireciona para `/login` se não logado
- ✅ **Autorização**: Verifica perfil do usuário
- ✅ **Flash messages**: Mensagens de erro informativas
- ✅ **Logging**: Registra tentativas de acesso não autorizado
- ✅ **Case-insensitive**: Admin = admin = ADMIN
- ✅ **Injeção de dependência**: `usuario_logado` é injetado automaticamente

---

## Validação de Senha Forte

### Requisitos de Senha

- Mínimo **8 caracteres**
- Pelo menos **1 letra maiúscula** (A-Z)
- Pelo menos **1 letra minúscula** (a-z)
- Pelo menos **1 número** (0-9)
- Pelo menos **1 caractere especial** (`!@#$%^&*(),.?":{}|<>`)

### Uso em DTOs

```python
from pydantic import BaseModel, field_validator
from utils.security import validar_forca_senha

class CadastroDTO(BaseModel):
    email: str
    senha: str
    confirmar_senha: str

    @field_validator('senha')
    @classmethod
    def validar_senha_forte(cls, v: str) -> str:
        valida, mensagem = validar_forca_senha(v)
        if not valida:
            raise ValueError(mensagem)
        return v

    @model_validator(mode='after')
    def validar_senhas_coincidem(self):
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não coincidem")
        return self
```

### Validadores Pré-configurados

```python
from utils.validacoes_dto import VALIDADOR_SENHA_FORTE

class CadastroDTO(BaseModel):
    senha: str

    _validar = field_validator('senha')(VALIDADOR_SENHA_FORTE)
```

---

## Rate Limiting

### Proteção Contra Força Bruta

```python
from utils.auth_decorator import SimpleRateLimiter
from util.config import RATE_LIMIT_LOGIN_MAX, RATE_LIMIT_LOGIN_MINUTOS

# Criar limiter
login_limiter = SimpleRateLimiter(
    max_tentativas=RATE_LIMIT_LOGIN_MAX,
    janela_minutos=RATE_LIMIT_LOGIN_MINUTOS
)

@router.post("/login")
async def login(request: Request, email: str, senha: str):
    ip = request.client.host if request.client else "unknown"

    # Verificar rate limit
    if not login_limiter.verificar(ip):
        return {"erro": f"Muitas tentativas. Aguarde {RATE_LIMIT_LOGIN_MINUTOS} min."}

    # ... processar login ...

    # Limpar tentativas após login bem-sucedido
    if login_bem_sucedido:
        login_limiter.limpar_tentativas(ip)

    return {"sucesso": True}
```

### Configuração (via .env)

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

---

## Logging Profissional

### Logger Centralizado

```python
from utils.logger_config import logger

# Níveis de log
logger.debug("Informação de debug")
logger.info("Informação geral")
logger.warning("Aviso")
logger.error("Erro")
logger.critical("Erro crítico")

# Exemplos de uso
logger.info(f"Usuário {email} fez login")
logger.warning(f"Tentativa de acesso não autorizado: {email}")
logger.error(f"Erro ao enviar email: {e}")
```

### Configuração de Níveis

Arquivo `.env`:

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Arquivos de Log

- **Localização**: `logs/obratto.log`
- **Rotação**: Automática (10MB por arquivo)
- **Backup**: 10 arquivos mantidos
- **Console**: Logs também aparecem no terminal

---

## Recuperação de Senha via Email

### Configuração do Resend.com

1. Criar conta em [resend.com](https://resend.com)
2. Obter API Key em: https://resend.com/api-keys
3. Adicionar ao `.env`:

```env
RESEND_API_KEY=re_123abc...
RESEND_FROM_EMAIL=noreply@seudominio.com
RESEND_FROM_NAME=OBRATTO
```

### Uso do EmailService

```python
from utils.email_service import email_service
from utils.security import gerar_token_redefinicao, obter_data_expiracao_token
from data.usuario import usuario_repo

@router.post("/esqueci-senha")
async def esqueci_senha(request: Request, email: str):
    usuario = usuario_repo.obter_usuario_por_email(email)

    if usuario:
        # Gerar token
        token = gerar_token_redefinicao()
        data_expiracao = obter_data_expiracao_token(horas=1)

        # Salvar token no banco
        usuario.token_redefinicao = token
        usuario.data_token = data_expiracao
        usuario_repo.atualizar_usuario(usuario)

        # Enviar email
        email_service.enviar_recuperacao_senha(
            para_email=usuario.email,
            para_nome=usuario.nome,
            token=token
        )

    return {"mensagem": "Se o email existir, você receberá instruções."}
```

### Templates de Email Disponíveis

```python
# Recuperação de senha
email_service.enviar_recuperacao_senha(email, nome, token)

# Boas-vindas após cadastro
email_service.enviar_boas_vindas(email, nome, perfil)

# Email genérico
email_service.enviar_email(
    para_email="user@example.com",
    para_nome="João",
    assunto="Assunto",
    html="<h1>HTML</h1>",
    texto="Texto plano"
)
```

---

## Flash Messages

### Uso em Rotas

```python
from utils.flash_messages import informar_sucesso, informar_erro, informar_aviso, informar_info

@router.post("/login")
async def login(request: Request, ...):
    if login_bem_sucedido:
        informar_sucesso(request, "Login realizado com sucesso!")
        return RedirectResponse("/dashboard")
    else:
        informar_erro(request, "Email ou senha inválidos")
        return RedirectResponse("/login")
```

### Exibição em Templates

```html
{% set mensagens = obter_mensagens(request) %}
{% for msg in mensagens %}
    <div class="alert alert-{{ msg.tipo }}">
        {{ msg.texto }}
    </div>
{% endfor %}
```

### Tipos de Mensagem

- `sucesso` → Operação bem-sucedida (verde)
- `erro` → Erro ou validação falhou (vermelho)
- `aviso` → Aviso importante (amarelo)
- `info` → Informação geral (azul)

---

## Testes

### Teste Manual

```bash
# 1. Login com credenciais válidas
curl -X POST http://localhost:8000/login \
  -d "email=admin@obratto.com&senha=Admin@123"

# 2. Tentar acessar rota protegida sem login
curl http://localhost:8000/admin

# 3. Cadastro com senha fraca (deve falhar)
curl -X POST http://localhost:8000/cadastro/cliente \
  -d "email=teste@example.com&senha=123"

# 4. Cadastro com senha forte (deve funcionar)
curl -X POST http://localhost:8000/cadastro/cliente \
  -d "email=teste@example.com&senha=Admin@123&confirmar_senha=Admin@123"

# 5. Rate limiting - fazer 6 tentativas de login (6ª deve bloquear)
for i in {1..6}; do
  curl -X POST http://localhost:8000/login \
    -d "email=teste@example.com&senha=errada"
done
```

### Verificar Logs

```bash
tail -f logs/obratto.log
```

---

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'dotenv'"

```bash
pip install python-dotenv
```

### Erro: "ModuleNotFoundError: No module named 'resend'"

```bash
pip install resend
```

### Email não envia

1. Verifique se `RESEND_API_KEY` está configurada no `.env`
2. Verifique logs: `cat logs/obratto.log | grep -i email`
3. Teste manualmente:

```python
from utils.email_service import email_service

resultado = email_service.enviar_email(
    para_email="seu@email.com",
    para_nome="Teste",
    assunto="Teste",
    html="<h1>Teste</h1>"
)
print(f"Email enviado: {resultado}")
```

### Rate limit não funciona

- Certifique-se de que `.env` está carregado
- Verifique configurações em `util/config.py`
- Logs devem mostrar: `[WARNING] Rate limit excedido para...`

### Logs não aparecem

- Verifique se o diretório `logs/` existe
- Verifique permissões de escrita
- Ajuste `LOG_LEVEL` no `.env` para `DEBUG`

---

## Boas Práticas

### 1. Nunca Commitar .env

```bash
# Adicionar ao .gitignore
echo ".env" >> .gitignore
```

### 2. Usar Enum para Perfis

```python
# ✅ Correto
from util.perfis import Perfil
if usuario.perfil == Perfil.ADMINISTRADOR.value:
    ...

# ❌ Errado
if usuario.perfil == "admin":  # NÃO FAZER!
    ...
```

### 3. Validar Senhas no Cadastro

```python
# ✅ Sempre use validação forte no cadastro
from utils.security import validar_forca_senha

valida, mensagem = validar_forca_senha(senha)
if not valida:
    return erro(mensagem)
```

### 4. Log de Eventos Importantes

```python
from utils.logger_config import logger

# Sempre logar:
logger.info(f"Login: {email}")
logger.warning(f"Acesso negado: {email}")
logger.error(f"Erro ao processar: {e}")
```

### 5. Rate Limiting em Rotas Sensíveis

Sempre adicione rate limiting em:
- Login
- Cadastro
- Recuperação de senha
- Envio de emails

---

## Próximos Passos (Opcionais)

1. **2FA (Autenticação de Dois Fatores)** - TOTP com Google Authenticator
2. **OAuth** - Login via Google, GitHub, etc.
3. **Auditoria** - Tabela de logs de login/tentativas
4. **Bloqueio de Conta** - Após N tentativas falhas
5. **Confirmação de Email** - Token de ativação após cadastro
6. **Sessões Persistentes** - "Lembrar-me" com cookies
7. **Força de Senha Visual** - Indicador no frontend
8. **Rate Limiting Avançado** - Redis ou similar em produção

---

## Suporte

Para dúvidas ou problemas:

1. Verifique os logs: `cat logs/obratto.log`
2. Consulte esta documentação
3. Entre em contato com a equipe de desenvolvimento

---

**Documentação atualizada em: Janeiro 2025**
**Versão do Sistema: 1.0.0**
