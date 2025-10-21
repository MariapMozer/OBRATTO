---
description: Implementa sistema completo de autenticação/autorização FastAPI
---

# Criar Sistema de Autenticação/Autorização FastAPI

Analisa, remove (se necessário) e implementa um sistema completo de autenticação e autorização para FastAPI, baseado em sessões, com perfis de usuário, recuperação de senha, validação robusta e interface web profissional.

## FASE 1: Análise do Projeto Alvo

### 1.1 Verificar Sistema Existente

Execute análise para identificar componentes de autenticação existentes:

```bash
# Buscar por imports relacionados a auth
rg -i "(jwt|token|oauth|auth|login|session)" --type py

# Buscar por decoradores de autenticação
rg -i "(@login_required|@require|@authenticate|@depends)" --type py

# Verificar modelos de usuário
rg -i "(class.*user|usuario)" --type py

# Verificar rotas de auth
rg -i "(login|logout|register|cadastr)" --type py
```

### 1.2 Documentar Sistema Atual

Crie um arquivo temporário `auth_analysis.md` documentando:
- Tipo de autenticação (JWT, Session, OAuth, Basic)
- Arquivos envolvidos (models, routes, middleware)
- Bibliotecas usadas
- Estrutura de banco de dados
- Campos customizados do modelo User/Usuario
- Perfis/roles existentes

### 1.3 Confirmar com Usuário

**IMPORTANTE:** Antes de prosseguir, confirme com o usuário:
1. Lista completa de perfis/roles necessários (ex: Admin, Cliente, Vendedor, etc.)
2. Campos adicionais do usuário além dos padrão (nome, email, senha, perfil)
3. Se deve remover sistema existente ou adaptar
4. Se precisa de recuperação de senha via email

## FASE 2: Remoção do Sistema Antigo (se aplicável)

Se houver sistema existente, remover nesta ordem:

### 2.1 Backup
```bash
# Criar backup antes de qualquer remoção
git add -A
git commit -m "Backup antes de remover autenticação antiga"
```

### 2.2 Remover Componentes

1. **Middlewares de Auth** (geralmente em `main.py` ou `app.py`)
2. **Rotas de Auth** (arquivos `*auth*.py`, `*login*.py`)
3. **Modelos de Auth** (classes User, Token, etc.)
4. **DTOs de Auth** (validação de login, registro)
5. **Dependências de Auth** (funções `get_current_user`, decorators)
6. **Templates de Auth** (páginas de login, registro)
7. **Desinstalar bibliotecas não usadas:**
   ```bash
   pip uninstall python-jose passlib[bcrypt] python-multipart
   ```

## FASE 3: Implementação do Novo Sistema

### 3.1 Instalar Dependências

Adicione ao `requirements.txt` ou instale diretamente:

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-dotenv>=1.0.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
resend>=0.7.0
jinja2>=3.1.2
itsdangerous>=2.1.2
```

```bash
pip install -r requirements.txt
```

### 3.2 Criar Estrutura de Diretórios

```bash
mkdir -p util dtos model repo sql routes/auth templates/auth static/js static/css
```

### 3.3 Configuração (.env)

Crie ou atualize `.env`:

```env
# Aplicação
APP_NAME=Nome da Aplicação
BASE_URL=http://localhost:8000
SECRET_KEY=sua-chave-secreta-super-segura-mude-em-producao-$(openssl rand -hex 32)
RUNNING_MODE=Development

# Banco de Dados
DATABASE_PATH=database.db

# Servidor
HOST=0.0.0.0
PORT=8000
RELOAD=True

# Email (Resend.com) - Opcional
RESEND_API_KEY=
RESEND_FROM_EMAIL=noreply@seudominio.com
RESEND_FROM_NAME=Sistema

# Logging
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_LOGIN_MAX=5
RATE_LIMIT_LOGIN_MINUTOS=5
RATE_LIMIT_CADASTRO_MAX=3
RATE_LIMIT_CADASTRO_MINUTOS=10
RATE_LIMIT_ESQUECI_SENHA_MAX=1
RATE_LIMIT_ESQUECI_SENHA_MINUTOS=1
```

### 3.4 Arquivo: util/config.py

```python
"""
Módulo de configurações centralizadas da aplicação.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# === Configurações da Aplicação ===
APP_NAME = os.getenv("APP_NAME", "Sistema Web")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-super-segura")

# === Configurações do Banco de Dados ===
DATABASE_PATH = os.getenv("DATABASE_PATH", "database.db")

# === Configurações de Logging ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# === Configurações de Email (Resend.com) ===
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "noreply@seudominio.com")
RESEND_FROM_NAME = os.getenv("RESEND_FROM_NAME", APP_NAME)

# === Configurações do Servidor ===
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "True").lower() == "true"

# === Modo de Execução ===
RUNNING_MODE = os.getenv("RUNNING_MODE", "Production")
IS_DEVELOPMENT = RUNNING_MODE.lower() == "development"

# === Configurações de Rate Limiting ===
RATE_LIMIT_LOGIN_MAX = int(os.getenv("RATE_LIMIT_LOGIN_MAX", "5"))
RATE_LIMIT_LOGIN_MINUTOS = int(os.getenv("RATE_LIMIT_LOGIN_MINUTOS", "5"))
RATE_LIMIT_CADASTRO_MAX = int(os.getenv("RATE_LIMIT_CADASTRO_MAX", "3"))
RATE_LIMIT_CADASTRO_MINUTOS = int(os.getenv("RATE_LIMIT_CADASTRO_MINUTOS", "10"))
RATE_LIMIT_ESQUECI_SENHA_MAX = int(os.getenv("RATE_LIMIT_ESQUECI_SENHA_MAX", "1"))
RATE_LIMIT_ESQUECI_SENHA_MINUTOS = int(os.getenv("RATE_LIMIT_ESQUECI_SENHA_MINUTOS", "1"))

# === Versão da Aplicação ===
VERSION = "1.0.0"
```

### 3.5 Arquivo: util/perfis.py

**IMPORTANTE:** Adapte os perfis conforme necessidade do projeto!

```python
from enum import Enum
from typing import Optional

class Perfil(str, Enum):
    """
    Enum centralizado para perfis de usuário.

    FONTE ÚNICA DA VERDADE para perfis no sistema.
    SEMPRE use este Enum, NUNCA strings literais.

    INSTRUÇÕES DE CUSTOMIZAÇÃO:
    - Adicione/remova perfis conforme necessidade do projeto
    - Mantenha valores em português ou inglês conforme padrão do projeto
    - Exemplo: ADMIN = "Administrador" ou ADMIN = "admin"
    """

    # PERFIS DO SISTEMA (CUSTOMIZAR AQUI) ######################
    ADMIN = "Administrador"
    CLIENTE = "Cliente"
    VENDEDOR = "Vendedor"
    # FIM DOS PERFIS ############################################

    def __str__(self) -> str:
        return self.value

    @classmethod
    def valores(cls) -> list[str]:
        """Retorna lista de todos os valores de perfis"""
        return [perfil.value for perfil in cls]

    @classmethod
    def existe(cls, valor: str) -> bool:
        """Verifica se um valor de perfil é válido"""
        return valor in cls.valores()

    @classmethod
    def from_string(cls, valor: str) -> Optional['Perfil']:
        """Converte string para Enum Perfil"""
        try:
            return cls(valor)
        except ValueError:
            return None

    @classmethod
    def validar(cls, valor: str) -> str:
        """Valida e retorna o valor, levantando exceção se inválido"""
        if not cls.existe(valor):
            raise ValueError(f'Perfil inválido: {valor}. Use: {", ".join(cls.valores())}')
        return valor
```

### 3.6 Arquivo: util/db_util.py

```python
import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')

@contextmanager
def get_connection():
    """Context manager para conexão com banco de dados"""
    register_adapters()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def adapt_datetime(dt: datetime) -> str:
    """Adaptador para converter datetime para string ISO"""
    return dt.isoformat()

def convert_datetime(s: bytes) -> datetime:
    """Conversor para converter string ISO para datetime"""
    return datetime.fromisoformat(s.decode())

def register_adapters() -> None:
    """Registra adaptadores customizados para datetime"""
    sqlite3.register_adapter(datetime, adapt_datetime)
    sqlite3.register_converter("TIMESTAMP", convert_datetime)
```

### 3.7 Arquivo: util/logger_config.py

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from util.config import LOG_LEVEL

# Criar diretório de logs
Path("logs").mkdir(exist_ok=True)

# Configurar logger
logger = logging.getLogger("app")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# Handler para arquivo com rotação
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(levelname)s - %(message)s')
)
logger.addHandler(console_handler)
```

### 3.8 Arquivo: util/security.py

```python
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_hash_senha(senha: str) -> str:
    """Cria hash da senha usando bcrypt"""
    return pwd_context.hash(senha)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se senha corresponde ao hash"""
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_token_redefinicao() -> str:
    """Gera token seguro para redefinição de senha"""
    return secrets.token_urlsafe(32)

def obter_data_expiracao_token(horas: int = 1) -> str:
    """Retorna data de expiração do token"""
    expiracao = datetime.now() + timedelta(hours=horas)
    return expiracao.isoformat()
```

### 3.9 Arquivo: util/senha_util.py

```python
import re
from typing import Tuple

def validar_forca_senha(senha: str) -> Tuple[bool, str]:
    """
    Valida força da senha.
    Retorna: (é_válida, mensagem)
    """
    if len(senha) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"

    if not re.search(r"[A-Z]", senha):
        return False, "Senha deve conter pelo menos uma letra maiúscula"

    if not re.search(r"[a-z]", senha):
        return False, "Senha deve conter pelo menos uma letra minúscula"

    if not re.search(r"\d", senha):
        return False, "Senha deve conter pelo menos um número"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False, "Senha deve conter pelo menos um caractere especial"

    return True, "Senha válida"

def calcular_nivel_senha(senha: str) -> str:
    """Retorna: fraca, média, forte"""
    pontos = 0

    if len(senha) >= 8: pontos += 1
    if len(senha) >= 12: pontos += 1
    if re.search(r"[A-Z]", senha): pontos += 1
    if re.search(r"[a-z]", senha): pontos += 1
    if re.search(r"\d", senha): pontos += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha): pontos += 1

    if pontos <= 2: return "fraca"
    if pontos <= 4: return "média"
    return "forte"
```

### 3.10 Arquivo: util/flash_messages.py

```python
from fastapi import Request
from typing import Literal

TipoMensagem = Literal["sucesso", "erro", "aviso", "info"]

def adicionar_mensagem(
    request: Request,
    mensagem: str,
    tipo: TipoMensagem = "info"
):
    """Adiciona mensagem flash à sessão"""
    if "mensagens" not in request.session:
        request.session["mensagens"] = []

    request.session["mensagens"].append({
        "texto": mensagem,
        "tipo": tipo
    })

def informar_sucesso(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "sucesso")

def informar_erro(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "erro")

def informar_aviso(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "aviso")

def informar_info(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "info")

def obter_mensagens(request: Request) -> list:
    """Obtém e limpa mensagens da sessão"""
    mensagens = request.session.pop("mensagens", [])
    return mensagens
```

### 3.11 Arquivo: util/template_util.py

```python
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
from util.flash_messages import obter_mensagens
from util.config import APP_NAME, VERSION

def criar_templates(pasta: str):
    """Cria Jinja2Templates com funções globais customizadas"""
    env = Environment(loader=FileSystemLoader("templates"))

    # Adicionar função global para obter mensagens
    env.globals['obter_mensagens'] = obter_mensagens

    # Adicionar variáveis globais de configuração
    env.globals['APP_NAME'] = APP_NAME
    env.globals['VERSION'] = VERSION

    templates = Jinja2Templates(env=env)
    return templates
```

### 3.12 Arquivo: util/auth_decorator.py

```python
from fastapi import Request, status
from fastapi.responses import RedirectResponse
from functools import wraps
from typing import List, Optional
from util.logger_config import logger
from util.flash_messages import informar_erro

def criar_sessao(request: Request, usuario: dict):
    """Cria sessão de usuário"""
    request.session["usuario_logado"] = usuario

def destruir_sessao(request: Request):
    """Destroi sessão de usuário"""
    request.session.clear()

def obter_usuario_logado(request: Request) -> Optional[dict]:
    """Obtém usuário logado da sessão"""
    return request.session.get("usuario_logado")

def esta_logado(request: Request) -> bool:
    """Verifica se usuário está logado"""
    return "usuario_logado" in request.session

def requer_autenticacao(perfis_permitidos: Optional[List[str]] = None):
    """
    Decorator para exigir autenticação e autorização

    Args:
        perfis_permitidos: Lista de perfis que podem acessar (None = qualquer logado)

    Exemplo:
        @requer_autenticacao([Perfil.ADMIN.value])
        @requer_autenticacao()  # qualquer usuário logado
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request') or args[0]

            # Verificar se está logado
            usuario = obter_usuario_logado(request)
            if not usuario:
                logger.warning(f"Tentativa de acesso não autenticado a {request.url.path}")
                informar_erro(request, "Você precisa estar autenticado para acessar esta página.")
                return RedirectResponse(
                    f"/login?redirect={request.url.path}",
                    status_code=status.HTTP_303_SEE_OTHER
                )

            # Verificar perfil se especificado
            if perfis_permitidos:
                perfil_usuario = usuario.get("perfil")
                if perfil_usuario not in perfis_permitidos:
                    logger.warning(
                        f"Usuário {usuario.get('email')} tentou acessar {request.url.path} "
                        f"sem permissão (perfil: {perfil_usuario})"
                    )
                    informar_erro(request, "Você não tem permissão para acessar esta página.")
                    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

            # Injetar usuario_logado nos kwargs
            kwargs['usuario_logado'] = usuario
            return await func(*args, **kwargs)

        return wrapper
    return decorator
```

### 3.13 Arquivo: util/email_service.py

```python
import os
import resend
from typing import Optional
from util.logger_config import logger

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('RESEND_API_KEY')
        self.from_email = os.getenv('RESEND_FROM_EMAIL', 'noreply@seudominio.com')
        self.from_name = os.getenv('RESEND_FROM_NAME', 'Sistema')

        if self.api_key:
            resend.api_key = self.api_key

    def enviar_email(
        self,
        para_email: str,
        para_nome: str,
        assunto: str,
        html: str,
        texto: Optional[str] = None
    ) -> bool:
        """Envia e-mail via Resend.com"""
        if not self.api_key:
            logger.warning("RESEND_API_KEY não configurada")
            return False

        params = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [para_email],
            "subject": assunto,
            "html": html
        }

        try:
            email = resend.Emails.send(params)
            logger.info(f"E-mail enviado para {para_email} - ID: {email.get('id', 'N/A')}")
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail: {e}")
            return False

    def enviar_recuperacao_senha(self, para_email: str, para_nome: str, token: str) -> bool:
        """Envia e-mail de recuperação de senha"""
        url_recuperacao = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/redefinir-senha?token={token}"

        html = f"""
        <html>
        <body>
            <h2>Recuperação de Senha</h2>
            <p>Olá {para_nome},</p>
            <p>Você solicitou a recuperação de senha.</p>
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <a href="{url_recuperacao}">Redefinir Senha</a>
            <p>Este link expira em 1 hora.</p>
            <p>Se você não solicitou esta recuperação, ignore este e-mail.</p>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Recuperação de Senha",
            html=html
        )

    def enviar_boas_vindas(self, para_email: str, para_nome: str) -> bool:
        """Envia e-mail de boas-vindas"""
        html = f"""
        <html>
        <body>
            <h2>Bem-vindo(a)!</h2>
            <p>Olá {para_nome},</p>
            <p>Seu cadastro foi realizado com sucesso!</p>
            <p>Agora você pode acessar o sistema com seu e-mail e senha.</p>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Bem-vindo ao Sistema",
            html=html
        )

# Instância global
email_service = EmailService()
```

### 3.14 Arquivo: model/usuario_model.py

**IMPORTANTE:** Adicione campos customizados conforme necessidade do projeto!

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    """
    Model de usuário do sistema.

    INSTRUÇÕES DE CUSTOMIZAÇÃO:
    - Adicione campos extras conforme necessidade (telefone, cpf, etc.)
    - Mantenha campos obrigatórios: id, nome, email, senha, perfil
    - Use Optional[] para campos opcionais
    """
    id: int
    nome: str
    email: str
    senha: str
    perfil: str
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None

    # CAMPOS CUSTOMIZADOS (ADICIONAR AQUI SE NECESSÁRIO) #######
    # telefone: Optional[str] = None
    # cpf: Optional[str] = None
    # data_nascimento: Optional[str] = None
    # endereco: Optional[str] = None
    # cidade: Optional[str] = None
    # estado: Optional[str] = None
    # cep: Optional[str] = None
    # foto: Optional[str] = None
    # ############################################################
```

### 3.15 Arquivo: sql/usuario_sql.py

**IMPORTANTE:** Adapte CREATE TABLE conforme campos customizados!

```python
# INSTRUÇÕES DE CUSTOMIZAÇÃO:
# - Adapte CRIAR_TABELA adicionando colunas para campos customizados
# - Adapte INSERIR e ALTERAR conforme novos campos
# - Exemplo: telefone TEXT, cpf TEXT UNIQUE, etc.

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL,
    token_redefinicao TEXT,
    data_token DATETIME,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    -- ADICIONAR CAMPOS CUSTOMIZADOS AQUI --
    -- , telefone TEXT
    -- , cpf TEXT UNIQUE
)
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, perfil)
VALUES (?, ?, ?, ?)
"""

ALTERAR = """
UPDATE usuario
SET nome = ?, email = ?, perfil = ?
WHERE id = ?
"""

ALTERAR_SENHA = """
UPDATE usuario
SET senha = ?
WHERE id = ?
"""

EXCLUIR = "DELETE FROM usuario WHERE id = ?"

OBTER_POR_ID = "SELECT * FROM usuario WHERE id = ?"

OBTER_TODOS = "SELECT * FROM usuario ORDER BY nome"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM usuario"

OBTER_POR_EMAIL = "SELECT * FROM usuario WHERE email = ?"

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao = ?, data_token = ?
WHERE email = ?
"""

OBTER_POR_TOKEN = """
SELECT * FROM usuario
WHERE token_redefinicao = ?
"""

LIMPAR_TOKEN = """
UPDATE usuario
SET token_redefinicao = NULL, data_token = NULL
WHERE id = ?
"""

OBTER_TODOS_POR_PERFIL = """
SELECT * FROM usuario
WHERE perfil = ?
ORDER BY nome
"""
```

### 3.16 Arquivo: repo/usuario_repo.py

**IMPORTANTE:** Adapte funções conforme campos customizados!

```python
from typing import Optional
from model.usuario_model import Usuario
from sql.usuario_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.perfil
            # ADICIONAR CAMPOS CUSTOMIZADOS AQUI
            # , usuario.telefone
            # , usuario.cpf
        ))
        return cursor.lastrowid

def alterar(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            usuario.nome,
            usuario.email,
            usuario.perfil,
            usuario.id
            # ADICIONAR CAMPOS CUSTOMIZADOS AQUI
        ))
        return cursor.rowcount > 0

def atualizar_senha(id: int, senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_SENHA, (senha, id))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"]
                # ADICIONAR CAMPOS CUSTOMIZADOS AQUI
                # , telefone=row.get("telefone")
                # , cpf=row.get("cpf")
            )
        return None

def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                token_redefinicao=row.get("token_redefinicao"),
                data_token=row.get("data_token"),
                data_cadastro=row.get("data_cadastro")
                # ADICIONAR CAMPOS CUSTOMIZADOS
            )
            for row in rows
        ]

def obter_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                token_redefinicao=row.get("token_redefinicao"),
                data_token=row.get("data_token")
            )
        return None

def atualizar_token(email: str, token: str, data_expiracao: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TOKEN, (token, data_expiracao, email))
        return cursor.rowcount > 0

def obter_por_token(token: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_TOKEN, (token,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                perfil=row["perfil"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"]
            )
        return None

def limpar_token(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(LIMPAR_TOKEN, (id,))
        return cursor.rowcount > 0
```

### 3.17 Arquivo: dtos/validators.py (Validadores Reutilizáveis)

```python
from typing import Callable
import re

def validar_email() -> Callable:
    """Validador de e-mail"""
    def validator(v: str) -> str:
        if not v or not v.strip():
            raise ValueError("E-mail é obrigatório")

        v = v.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(pattern, v):
            raise ValueError("E-mail inválido")

        return v
    return validator

def validar_senha_forte() -> Callable:
    """Validador de senha forte"""
    def validator(v: str) -> str:
        if not v:
            raise ValueError("Senha é obrigatória")

        if len(v) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula")

        if not re.search(r"[a-z]", v):
            raise ValueError("Senha deve conter pelo menos uma letra minúscula")

        if not re.search(r"\d", v):
            raise ValueError("Senha deve conter pelo menos um número")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Senha deve conter pelo menos um caractere especial")

        return v
    return validator

def validar_nome_pessoa() -> Callable:
    """Validador de nome de pessoa"""
    def validator(v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Nome é obrigatório")

        v = v.strip()

        if len(v) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")

        if len(v) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")

        return v
    return validator

def validar_string_obrigatoria(
    nome_campo: str = "Campo",
    tamanho_minimo: int = 1,
    tamanho_maximo: int = 255
) -> Callable:
    """Validador genérico de string obrigatória"""
    def validator(v: str) -> str:
        if not v or not v.strip():
            raise ValueError(f"{nome_campo} é obrigatório")

        v = v.strip()

        if len(v) < tamanho_minimo:
            raise ValueError(f"{nome_campo} deve ter no mínimo {tamanho_minimo} caracteres")

        if len(v) > tamanho_maximo:
            raise ValueError(f"{nome_campo} deve ter no máximo {tamanho_maximo} caracteres")

        return v
    return validator
```

### 3.18 Arquivo: dtos/auth_dto.py

```python
from pydantic import BaseModel, field_validator, model_validator
from dtos.validators import (
    validar_email,
    validar_senha_forte,
    validar_nome_pessoa,
    validar_string_obrigatoria,
)
from util.perfis import Perfil

class LoginDTO(BaseModel):
    """DTO para validação de dados de login"""

    email: str
    senha: str

    _validar_email = field_validator("email")(validar_email())
    _validar_senha = field_validator("senha")(validar_senha_forte())

class CadastroDTO(BaseModel):
    """DTO para validação de dados de cadastro"""

    perfil: str
    nome: str
    email: str
    senha: str
    confirmar_senha: str

    @field_validator("perfil")
    @classmethod
    def validar_perfil(cls, v: str) -> str:
        """
        Valida perfil - apenas perfis não-admin permitidos no cadastro público

        CUSTOMIZAR: Adapte conforme perfis que podem se auto-cadastrar
        """
        perfis_permitidos = [p.value for p in Perfil if p != Perfil.ADMIN]
        if v not in perfis_permitidos:
            raise ValueError(f"Perfil inválido. Escolha entre: {', '.join(perfis_permitidos)}")
        return v

    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
    _validar_senha = field_validator("senha")(validar_senha_forte())
    _validar_confirmar = field_validator("confirmar_senha")(
        validar_string_obrigatoria("Confirmação de Senha", tamanho_minimo=8)
    )

    @model_validator(mode="after")
    def validar_senhas_coincidem(self) -> "CadastroDTO":
        """Valida se senha e confirmação são iguais"""
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não coincidem")
        return self

class RecuperacaoSenhaDTO(BaseModel):
    """DTO para validação de recuperação de senha"""

    email: str

    _validar_email = field_validator("email")(validar_email())

class RedefinirSenhaDTO(BaseModel):
    """DTO para validação de redefinição de senha"""

    token: str
    senha: str
    confirmar_senha: str

    _validar_token = field_validator("token")(validar_string_obrigatoria("Token"))
    _validar_senha = field_validator("senha")(validar_senha_forte())
    _validar_confirmar = field_validator("confirmar_senha")(validar_string_obrigatoria())

    @model_validator(mode="after")
    def validar_senhas_coincidem(self) -> "RedefinirSenhaDTO":
        """Valida se senha e confirmação são iguais"""
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não coincidem")
        return self
```

### 3.19 Arquivo: routes/auth_routes.py

**Arquivo completo no próximo bloco devido ao tamanho...**

Continue lendo o próximo arquivo `routes/auth_routes.py`:

```python
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import datetime
from collections import defaultdict
from datetime import timedelta

from dtos.auth_dto import LoginDTO, CadastroDTO, RecuperacaoSenhaDTO, RedefinirSenhaDTO
from model.usuario_model import Usuario
from repo import usuario_repo
from util.security import criar_hash_senha, verificar_senha, gerar_token_redefinicao, obter_data_expiracao_token
from util.email_service import email_service
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.perfis import Perfil
from util.config import (
    RATE_LIMIT_LOGIN_MAX,
    RATE_LIMIT_LOGIN_MINUTOS,
    RATE_LIMIT_CADASTRO_MAX,
    RATE_LIMIT_CADASTRO_MINUTOS,
    RATE_LIMIT_ESQUECI_SENHA_MAX,
    RATE_LIMIT_ESQUECI_SENHA_MINUTOS
)

router = APIRouter()
templates = criar_templates("templates")

# Rate limiter simples
class SimpleRateLimiter:
    def __init__(self, max_tentativas: int = 5, janela_minutos: int = 5):
        self.max_tentativas = max_tentativas
        self.janela = timedelta(minutes=janela_minutos)
        self.tentativas: defaultdict[str, list[datetime]] = defaultdict(list)

    def verificar(self, identificador: str) -> bool:
        """Retorna True se dentro do limite"""
        agora = datetime.now()
        self.tentativas[identificador] = [
            t for t in self.tentativas[identificador]
            if agora - t < self.janela
        ]

        if len(self.tentativas[identificador]) >= self.max_tentativas:
            return False

        self.tentativas[identificador].append(agora)
        return True

login_limiter = SimpleRateLimiter(RATE_LIMIT_LOGIN_MAX, RATE_LIMIT_LOGIN_MINUTOS)
cadastro_limiter = SimpleRateLimiter(RATE_LIMIT_CADASTRO_MAX, RATE_LIMIT_CADASTRO_MINUTOS)
esqueci_senha_limiter = SimpleRateLimiter(RATE_LIMIT_ESQUECI_SENHA_MAX, RATE_LIMIT_ESQUECI_SENHA_MINUTOS)

@router.get("/login")
async def get_login(request: Request):
    """Exibe formulário de login"""
    if request.session.get("usuario_logado"):
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    """Processa login do usuário"""
    try:
        # Rate limiting
        ip = request.client.host if request.client else "unknown"
        if not login_limiter.verificar(ip):
            informar_erro(request, "Muitas tentativas de login. Aguarde alguns minutos.")
            return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

        # Validar com DTO
        dto = LoginDTO(email=email, senha=senha)

        # Buscar usuário
        usuario = usuario_repo.obter_por_email(dto.email)

        # Verificar credenciais
        if not usuario or not verificar_senha(dto.senha, usuario.senha):
            informar_erro(request, "E-mail ou senha inválidos")
            logger.warning(f"Login falhou: {dto.email}")
            return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

        # Criar sessão
        request.session["usuario_logado"] = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }

        logger.info(f"Login bem-sucedido: {usuario.email}")
        informar_sucesso(request, f"Bem-vindo(a), {usuario.nome}!")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = [erro['msg'] for erro in e.errors()]
        informar_erro(request, " | ".join(erros))
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/logout")
async def logout(request: Request):
    """Faz logout do usuário"""
    email = request.session.get("usuario_logado", {}).get("email", "Usuário")
    request.session.clear()
    logger.info(f"Logout: {email}")
    informar_sucesso(request, "Logout realizado com sucesso!")
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    """Exibe formulário de cadastro"""
    if request.session.get("usuario_logado"):
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("auth/cadastro.html", {"request": request})

@router.post("/cadastrar")
async def post_cadastrar(
    request: Request,
    perfil: str = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    """Processa cadastro de novo usuário"""
    try:
        # Rate limiting
        ip = request.client.host if request.client else "unknown"
        if not cadastro_limiter.verificar(ip):
            informar_erro(request, f"Muitas tentativas. Aguarde {RATE_LIMIT_CADASTRO_MINUTOS} min.")
            return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)

        # Validar com DTO
        dto = CadastroDTO(
            perfil=perfil,
            nome=nome,
            email=email,
            senha=senha,
            confirmar_senha=confirmar_senha
        )

        # Verificar e-mail duplicado
        if usuario_repo.obter_por_email(dto.email):
            informar_erro(request, "E-mail já cadastrado")
            return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)

        # Criar usuário
        usuario = Usuario(
            id=0,
            nome=dto.nome,
            email=dto.email,
            senha=criar_hash_senha(dto.senha),
            perfil=dto.perfil
        )

        usuario_id = usuario_repo.inserir(usuario)

        if usuario_id:
            logger.info(f"Cadastro realizado: {usuario.email}")
            email_service.enviar_boas_vindas(usuario.email, usuario.nome)
            informar_sucesso(request, "Cadastro realizado! Faça login para continuar.")
            return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao cadastrar. Tente novamente.")
            return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = [erro['msg'] for erro in e.errors()]
        informar_erro(request, " | ".join(erros))
        return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    """Exibe formulário de recuperação de senha"""
    return templates.TemplateResponse("auth/esqueci_senha.html", {"request": request})

@router.post("/esqueci-senha")
async def post_esqueci_senha(request: Request, email: str = Form(...)):
    """Processa recuperação de senha"""
    try:
        # Rate limiting
        ip = request.client.host if request.client else "unknown"
        if not esqueci_senha_limiter.verificar(ip):
            informar_erro(request, "Muitas tentativas. Aguarde.")
            return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)

        dto = RecuperacaoSenhaDTO(email=email)
        usuario = usuario_repo.obter_por_email(dto.email)

        if usuario:
            token = gerar_token_redefinicao()
            data_expiracao = obter_data_expiracao_token(horas=1)
            usuario_repo.atualizar_token(usuario.email, token, data_expiracao)
            email_service.enviar_recuperacao_senha(usuario.email, usuario.nome, token)
            logger.info(f"Recuperação de senha: {usuario.email}")

        # Sempre mesma mensagem (segurança)
        informar_sucesso(request, "Se o e-mail existir, você receberá instruções.")
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = [erro['msg'] for erro in e.errors()]
        informar_erro(request, " | ".join(erros))
        return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/redefinir-senha")
async def get_redefinir_senha(request: Request, token: str):
    """Exibe formulário de redefinição de senha"""
    usuario = usuario_repo.obter_por_token(token)

    if not usuario or not usuario.data_token:
        informar_erro(request, "Token inválido ou expirado")
        return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)

    try:
        data_token = datetime.fromisoformat(usuario.data_token)
        if datetime.now() > data_token:
            informar_erro(request, "Token expirado")
            return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)
    except:
        informar_erro(request, "Token inválido")
        return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("auth/redefinir_senha.html", {"request": request, "token": token})

@router.post("/redefinir-senha")
async def post_redefinir_senha(
    request: Request,
    token: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    """Processa redefinição de senha"""
    try:
        dto = RedefinirSenhaDTO(token=token, senha=senha, confirmar_senha=confirmar_senha)
        usuario = usuario_repo.obter_por_token(dto.token)

        if not usuario or not usuario.data_token:
            informar_erro(request, "Token inválido")
            return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)

        try:
            data_token = datetime.fromisoformat(usuario.data_token)
            if datetime.now() > data_token:
                informar_erro(request, "Token expirado")
                return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)
        except:
            informar_erro(request, "Token inválido")
            return RedirectResponse("/esqueci-senha", status_code=status.HTTP_303_SEE_OTHER)

        # Atualizar senha
        senha_hash = criar_hash_senha(dto.senha)
        usuario_repo.atualizar_senha(usuario.id, senha_hash)
        usuario_repo.limpar_token(usuario.id)

        logger.info(f"Senha redefinida: {usuario.email}")
        informar_sucesso(request, "Senha redefinida! Faça login.")
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = [erro['msg'] for erro in e.errors()]
        informar_erro(request, " | ".join(erros))
        return RedirectResponse(f"/redefinir-senha?token={token}", status_code=status.HTTP_303_SEE_OTHER)
```

### 3.20 Integração no main.py

Adicione ao arquivo `main.py`:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from util.config import APP_NAME, SECRET_KEY, HOST, PORT, RELOAD, VERSION
from util.logger_config import logger
from repo import usuario_repo
from routes.auth_routes import router as auth_router

# Criar aplicação
app = FastAPI(title=APP_NAME, version=VERSION)

# Adicionar SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
logger.info("SessionMiddleware configurado")

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Criar tabela de usuários
usuario_repo.criar_tabela()
logger.info("Tabela 'usuario' criada/verificada")

# Incluir routers
app.include_router(auth_router, tags=["Autenticação"])
logger.info("Router de autenticação incluído")

if __name__ == "__main__":
    logger.info(f"Iniciando {APP_NAME} v{VERSION}")
    logger.info(f"Servidor: http://{HOST}:{PORT}")

    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD)
```

### 3.21 Templates HTML (Mínimos)

**Crie templates básicos - podem ser customizados com Bootstrap/Tailwind depois**

`templates/auth/login.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>

    {% set mensagens = obter_mensagens(request) %}
    {% for msg in mensagens %}
        <div class="alert-{{ msg.tipo }}">{{ msg.texto }}</div>
    {% endfor %}

    <form method="POST" action="/login">
        <label>E-mail:</label>
        <input type="email" name="email" required>

        <label>Senha:</label>
        <input type="password" name="senha" required>

        <button type="submit">Entrar</button>
    </form>

    <a href="/esqueci-senha">Esqueceu a senha?</a>
    <a href="/cadastrar">Criar conta</a>
</body>
</html>
```

`templates/auth/cadastro.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Cadastro</title>
    <script src="/static/js/password-validator.js"></script>
</head>
<body>
    <h1>Criar Conta</h1>

    {% set mensagens = obter_mensagens(request) %}
    {% for msg in mensagens %}
        <div class="alert-{{ msg.tipo }}">{{ msg.texto }}</div>
    {% endfor %}

    <form method="POST" action="/cadastrar">
        <label>Perfil:</label>
        <select name="perfil" required>
            <option value="Cliente">Cliente</option>
            <option value="Vendedor">Vendedor</option>
        </select>

        <label>Nome:</label>
        <input type="text" name="nome" required>

        <label>E-mail:</label>
        <input type="email" name="email" required>

        <label>Senha:</label>
        <input type="password" id="senha" name="senha" required>

        <label>Confirmar Senha:</label>
        <input type="password" id="confirmar_senha" name="confirmar_senha" required>

        <div id="senha-strength"></div>
        <div id="senha-match"></div>

        <button type="submit">Cadastrar</button>
    </form>

    <a href="/login">Já tem conta? Faça login</a>
</body>
</html>
```

`templates/auth/esqueci_senha.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Recuperar Senha</title></head>
<body>
    <h1>Recuperar Senha</h1>

    {% set mensagens = obter_mensagens(request) %}
    {% for msg in mensagens %}
        <div>{{ msg.texto }}</div>
    {% endfor %}

    <form method="POST">
        <label>E-mail:</label>
        <input type="email" name="email" required>
        <button type="submit">Enviar</button>
    </form>

    <a href="/login">Voltar</a>
</body>
</html>
```

`templates/auth/redefinir_senha.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Redefinir Senha</title></head>
<body>
    <h1>Redefinir Senha</h1>

    {% set mensagens = obter_mensagens(request) %}
    {% for msg in mensagens %}
        <div>{{ msg.texto }}</div>
    {% endfor %}

    <form method="POST">
        <input type="hidden" name="token" value="{{ token }}">

        <label>Nova Senha:</label>
        <input type="password" name="senha" required>

        <label>Confirmar Senha:</label>
        <input type="password" name="confirmar_senha" required>

        <button type="submit">Redefinir</button>
    </form>
</body>
</html>
```

### 3.22 JavaScript: static/js/password-validator.js

```javascript
/**
 * PasswordValidator - Sistema de validação de senha reutilizável
 */
class PasswordValidator {
    constructor(config) {
        this.config = { minLength: 8, showStrength: false, ...config };
        this.passwordField = document.getElementById(this.config.passwordFieldId);
        this.confirmPasswordField = this.config.confirmPasswordFieldId
            ? document.getElementById(this.config.confirmPasswordFieldId)
            : null;

        if (this.passwordField) this.init();
    }

    init() {
        if (this.config.showStrength && this.config.strengthBarId) {
            this.strengthBar = document.getElementById(this.config.strengthBarId);
            this.strengthText = document.getElementById(this.config.strengthTextId);
            this.passwordField.addEventListener('input', () => this.checkPasswordStrength());
        }

        if (this.confirmPasswordField && this.config.matchMessageId) {
            this.matchMessage = document.getElementById(this.config.matchMessageId);
            this.confirmPasswordField.addEventListener('input', () => this.checkPasswordMatch());
        }
    }

    checkPasswordStrength() {
        const password = this.passwordField.value;
        let strength = 0;

        if (password.length >= 8) strength += 25;
        if (/[A-Z]/.test(password)) strength += 25;
        if (/[a-z]/.test(password)) strength += 25;
        if (/\d/.test(password)) strength += 25;

        if (this.strengthBar) this.strengthBar.style.width = strength + '%';
        if (this.strengthText) {
            this.strengthText.textContent = strength >= 75 ? 'Forte' : strength >= 50 ? 'Média' : 'Fraca';
        }
    }

    checkPasswordMatch() {
        if (!this.confirmPasswordField || !this.matchMessage) return;

        const match = this.passwordField.value === this.confirmPasswordField.value;
        this.matchMessage.textContent = match ? '✓ Senhas coincidem' : '✗ Senhas não coincidem';
        this.matchMessage.style.color = match ? 'green' : 'red';
    }

    validateForm() {
        const password = this.passwordField.value;
        const confirmPassword = this.confirmPasswordField?.value;

        if (password.length < 8) {
            alert('Senha deve ter no mínimo 8 caracteres');
            return false;
        }

        if (!/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/\d/.test(password)) {
            alert('Senha deve conter maiúscula, minúscula e número');
            return false;
        }

        if (this.confirmPasswordField && password !== confirmPassword) {
            alert('Senhas não coincidem');
            return false;
        }

        return true;
    }
}

function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    field.type = field.type === 'password' ? 'text' : 'password';
}

window.PasswordValidator = PasswordValidator;
window.togglePassword = togglePassword;
```

## FASE 4: Testes

### 4.1 Testes Manuais

1. **Cadastro:**
   - Acesse `/cadastrar`
   - Crie conta com cada perfil disponível
   - Teste validações (email inválido, senhas diferentes, etc.)

2. **Login:**
   - Acesse `/login`
   - Faça login com usuário criado
   - Teste credenciais inválidas

3. **Logout:**
   - Acesse `/logout`
   - Verifique redirecionamento

4. **Recuperação de Senha:**
   - Acesse `/esqueci-senha`
   - Solicite recuperação
   - Verifique email (se configurado)
   - Acesse link e redefina senha

5. **Proteção de Rotas:**
   - Criar rota protegida:
   ```python
   from util.auth_decorator import requer_autenticacao

   @router.get("/dashboard")
   @requer_autenticacao()
   async def dashboard(request: Request, usuario_logado: dict):
       return {"user": usuario_logado}
   ```

### 4.2 Verificar Logs

```bash
tail -f logs/app.log
```

### 4.3 Verificar Banco de Dados

```bash
sqlite3 database.db "SELECT * FROM usuario;"
```

## FASE 5: Melhorias Opcionais

1. **UI Profissional:** Integrar Bootstrap/Tailwind nos templates
2. **Lembrar-me:** Adicionar cookie "remember_me"
3. **2FA:** Implementar autenticação de dois fatores
4. **OAuth:** Adicionar login social (Google, GitHub)
5. **Auditoria:** Log de tentativas de login
6. **Bloqueio de Conta:** Após N tentativas falhas
7. **Força de Senha:** Indicador visual no cadastro
8. **Confirmação de Email:** Token de ativação

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'X'"
```bash
pip install -r requirements.txt
```

### Problema: "Secret key not configured"
Gere nova chave:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Problema: Email não envia
- Verifique `RESEND_API_KEY` no `.env`
- Teste com conta Resend.com válida

### Problema: Sessão não persiste
- Verifique `SessionMiddleware` está registrado
- Verifique `SECRET_KEY` está configurado

## Checklist Final

- [ ] Perfis customizados definidos em `util/perfis.py`
- [ ] Campos customizados adicionados ao modelo/SQL/repo
- [ ] Dependências instaladas
- [ ] `.env` configurado
- [ ] Tabela criada no banco
- [ ] Login funciona
- [ ] Cadastro funciona
- [ ] Logout funciona
- [ ] Recuperação de senha funciona (se email configurado)
- [ ] Proteção de rotas testada
- [ ] Logs verificados
- [ ] Templates customizados (opcional)
- [ ] Documentação atualizada

## Próximos Passos

1. Implementar CRUD de usuários para admin
2. Adicionar perfil de usuário (foto, dados pessoais)
3. Melhorar UI dos templates
4. Implementar testes automatizados
5. Adicionar confirmação de email
6. Implementar rate limiting mais robusto
