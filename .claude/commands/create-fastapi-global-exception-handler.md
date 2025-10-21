---
description: Cria sistema completo de tratamento de exceções global para FastAPI
---

# Criar Sistema de Tratamento de Exceções Global para FastAPI

Implemente um sistema completo e robusto de tratamento de exceções global para aplicações FastAPI, seguindo as melhores práticas de desenvolvimento web.

## Contexto

Este comando cria um sistema de exception handlers que:
- Captura e trata todas as exceções de forma centralizada
- Diferencia comportamento entre Development e Production
- Loga erros de forma apropriada
- Exibe mensagens amigáveis para usuários
- Integra com sistema de flash messages
- Cria páginas de erro customizadas e profissionais

## Passos de Implementação

### 1. Criar Arquivo de Exception Handlers

Crie o arquivo `util/exception_handlers.py` com o seguinte conteúdo:

```python
from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from util.template_util import criar_templates
from util.flash_messages import informar_erro, informar_aviso
from util.logger_config import logger
from util.config import IS_DEVELOPMENT
import traceback

# Configurar templates de erro
templates = criar_templates("templates")


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler para exceções HTTP do Starlette/FastAPI

    - 401 (Unauthorized): Redireciona para login com mensagem
    - 403 (Forbidden): Redireciona para login com mensagem
    - 404 (Not Found): Exibe página de erro 404
    - Outros: Loga e retorna página de erro genérica
    """
    status_code = exc.status_code

    # Extensões de arquivos estáticos opcionais que não devem gerar warnings
    STATIC_OPTIONAL_EXTENSIONS = ('.map', '.ico', '.woff', '.woff2', '.ttf', '.eot')

    # Determinar nível de log baseado no tipo de recurso
    path_lower = request.url.path.lower()
    is_optional_static = status_code == 404 and path_lower.endswith(STATIC_OPTIONAL_EXTENSIONS)

    # Log da exceção com nível apropriado
    log_message = (
        f"HTTPException {status_code}: {exc.detail} - "
        f"Path: {request.url.path} - "
        f"IP: {request.client.host if request.client else 'unknown'}"
    )

    if is_optional_static:
        logger.debug(log_message)
    else:
        logger.warning(log_message)

    # 401 - Não autenticado
    if status_code == status.HTTP_401_UNAUTHORIZED:
        informar_erro(request, "Você precisa estar autenticado para acessar esta página.")
        return RedirectResponse(
            f"/login?redirect={request.url.path}",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # 403 - Sem permissão
    if status_code == status.HTTP_403_FORBIDDEN:
        informar_erro(request, "Você não tem permissão para acessar esta página.")
        return RedirectResponse(
            "/login",
            status_code=status.HTTP_303_SEE_OTHER
        )

    # 404 - Não encontrado
    if status_code == status.HTTP_404_NOT_FOUND:
        return templates.TemplateResponse(
            "errors/404.html",
            {"request": request},
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Outros erros HTTP - página de erro genérica
    context = {
        "request": request,
        "error_code": status_code,
        "error_message": exc.detail if IS_DEVELOPMENT else "Ocorreu um erro ao processar sua solicitação."
    }

    # Em desenvolvimento, adicionar detalhes técnicos
    if IS_DEVELOPMENT:
        context["error_details"] = {
            "type": type(exc).__name__,
            "detail": str(exc.detail),
            "path": request.url.path,
            "method": request.method
        }

    return templates.TemplateResponse(
        "errors/500.html",
        context,
        status_code=status_code
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler para erros de validação do Pydantic
    Loga o erro e exibe mensagem amigável
    """
    logger.warning(
        f"Erro de validação: {exc.errors()} - "
        f"Path: {request.url.path} - "
        f"Body: {exc.body}"
    )

    # Extrair mensagens de erro
    erros = []
    for error in exc.errors():
        campo = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        mensagem = error["msg"]
        erros.append(f"{campo}: {mensagem}" if campo else mensagem)

    # Mensagem amigável ou técnica dependendo do modo
    if IS_DEVELOPMENT:
        mensagem_flash = f"Dados inválidos: {'; '.join(erros)}"
        error_message = f"Erro de validação: {'; '.join(erros)}"
    else:
        mensagem_flash = "Os dados fornecidos são inválidos. Por favor, verifique e tente novamente."
        error_message = "Erro de validação de dados"

    informar_erro(request, mensagem_flash)

    context = {
        "request": request,
        "error_code": 422,
        "error_message": error_message
    }

    # Em desenvolvimento, adicionar detalhes técnicos
    if IS_DEVELOPMENT:
        context["error_details"] = {
            "type": "RequestValidationError",
            "errors": exc.errors(),
            "body": str(exc.body),
            "path": request.url.path,
            "method": request.method
        }

    return templates.TemplateResponse(
        "errors/500.html",
        context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handler genérico para todas as exceções não tratadas
    Loga o erro completo e exibe página de erro amigável
    """
    # Sempre logar o erro completo (independente do modo)
    logger.error(
        f"Exceção não tratada: {type(exc).__name__}: {str(exc)} - "
        f"Path: {request.url.path} - "
        f"IP: {request.client.host if request.client else 'unknown'}",
        exc_info=True
    )

    # Definir mensagem baseada no modo de execução
    if IS_DEVELOPMENT:
        error_message = f"{type(exc).__name__}: {str(exc)}"
    else:
        error_message = "Erro interno do servidor. Nossa equipe foi notificada."

    context = {
        "request": request,
        "error_code": 500,
        "error_message": error_message
    }

    # Em desenvolvimento, adicionar detalhes técnicos completos
    if IS_DEVELOPMENT:
        context["error_details"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
            "path": request.url.path,
            "method": request.method,
            "ip": request.client.host if request.client else 'unknown'
        }

    return templates.TemplateResponse(
        "errors/500.html",
        context,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
```

### 2. Registrar Handlers no main.py

Adicione as seguintes linhas no arquivo `main.py`, **ANTES** de registrar os routers:

```python
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from util.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

# Registrar Exception Handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
logger.info("Exception handlers registrados")
```

**IMPORTANTE:** A ordem de registro importa. Registre do mais específico (StarletteHTTPException) para o mais genérico (Exception).

### 3. Criar Template de Erro 404

Crie o arquivo `templates/errors/404.html`:

```html
{% extends "base_publica.html" %}

{% block titulo %}Página Não Encontrada{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6 text-center">
        <div class="error-container">
            <h1 class="error-code text-primary">404</h1>
            <h2 class="error-heading mb-4">Página Não Encontrada</h2>
            <div class="error-details mb-4">
                <p class="text-muted">
                    Desculpe, a página que você está procurando não existe ou foi movida.
                </p>
            </div>
            <div class="error-actions">
                <a href="/" class="btn btn-primary btn-lg me-2">
                    <i class="bi bi-house-door"></i> Ir para Página Inicial
                </a>
                {% if request.session.get('usuario_logado') %}
                <a href="/usuario" class="btn btn-outline-primary btn-lg">
                    <i class="bi bi-speedometer2"></i> Dashboard
                </a>
                {% else %}
                <a href="/login" class="btn btn-outline-primary btn-lg">
                    <i class="bi bi-box-arrow-in-right"></i> Fazer Login
                </a>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 4. Criar Template de Erro 500

Crie o arquivo `templates/errors/500.html`:

```html
{% extends "base_publica.html" %}

{% block titulo %}Erro no Servidor{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6 text-center">
        <div class="error-container">
            <h1 class="error-code text-danger">{{ error_code or 500 }}</h1>
            <h2 class="error-heading mb-4">Ops! Algo deu errado</h2>
            <div class="error-details mb-4">
                <p class="text-muted">
                    {% if error_message %}
                    {{ error_message }}
                    {% else %}
                    Ocorreu um erro interno no servidor. Nossa equipe já foi notificada e está trabalhando para resolver
                    o problema.
                    {% endif %}
                </p>
                <p class="text-muted">
                    Por favor, tente novamente em alguns instantes.
                </p>
            </div>
            <div class="error-actions">
                <a href="javascript:history.back()" class="btn btn-secondary btn-lg me-2">
                    <i class="bi bi-arrow-left"></i> Voltar
                </a>
                <a href="/" class="btn btn-primary btn-lg">
                    <i class="bi bi-house-door"></i> Ir para Página Inicial
                </a>
            </div>

            {% if error_details %}
            <div class="error-technical-details mt-5">
                <div class="alert alert-warning text-start" role="alert">
                    <h5 class="alert-heading">
                        <i class="bi bi-exclamation-triangle-fill"></i>
                        Detalhes Técnicos (Modo Development)
                    </h5>
                    <hr>
                    <p><strong>Tipo:</strong> {{ error_details.type }}</p>

                    {% if error_details.message %}
                    <p><strong>Mensagem:</strong> {{ error_details.message }}</p>
                    {% endif %}

                    {% if error_details.detail %}
                    <p><strong>Detalhe:</strong> {{ error_details.detail }}</p>
                    {% endif %}

                    <p><strong>Endpoint:</strong> {{ error_details.method }} {{ error_details.path }}</p>

                    {% if error_details.ip %}
                    <p><strong>IP:</strong> {{ error_details.ip }}</p>
                    {% endif %}

                    {% if error_details.errors %}
                    <p><strong>Erros de Validação:</strong></p>
                    <pre class="bg-light p-3 rounded"><code>{{ error_details.errors | tojson(indent=2) }}</code></pre>
                    {% endif %}

                    {% if error_details.body %}
                    <p><strong>Body:</strong></p>
                    <pre class="bg-light p-3 rounded"><code>{{ error_details.body }}</code></pre>
                    {% endif %}

                    {% if error_details.traceback %}
                    <p><strong>Traceback:</strong></p>
                    <pre class="bg-light p-3 rounded fs-small overflow-auto" style="max-height: 400px;"><code>{{ error_details.traceback }}</code></pre>
                    {% endif %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### 5. Adicionar Estilos CSS (Opcional)

Adicione ao seu arquivo CSS principal (ex: `static/css/custom.css`):

```css
/* Páginas de Erro */
.error-container {
    padding: 2rem 1rem;
}

.error-code {
    font-size: 8rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.error-heading {
    font-size: 2rem;
    font-weight: 600;
}

.error-details {
    font-size: 1.1rem;
}

.error-actions {
    margin-top: 2rem;
}

.error-technical-details {
    text-align: left;
}

.error-technical-details pre {
    max-height: 400px;
    overflow-y: auto;
}

@media (max-width: 768px) {
    .error-code {
        font-size: 5rem;
    }

    .error-heading {
        font-size: 1.5rem;
    }
}
```

## Dependências Necessárias

Certifique-se de que os seguintes módulos existam no projeto (ou adapte conforme necessário):

### util/config.py
Deve exportar:
- `IS_DEVELOPMENT`: boolean indicando se está em modo de desenvolvimento

```python
import os
from dotenv import load_dotenv

load_dotenv()

RUNNING_MODE = os.getenv("RUNNING_MODE", "Production")
IS_DEVELOPMENT = RUNNING_MODE.lower() == "development"
```

### util/flash_messages.py
Deve exportar:
- `informar_erro(request, mensagem)`: função para adicionar mensagens de erro à sessão
- `informar_aviso(request, mensagem)`: função para adicionar mensagens de aviso à sessão

```python
from fastapi import Request

def informar_erro(request: Request, mensagem: str):
    if "mensagens" not in request.session:
        request.session["mensagens"] = []
    request.session["mensagens"].append({"texto": mensagem, "tipo": "erro"})

def informar_aviso(request: Request, mensagem: str):
    if "mensagens" not in request.session:
        request.session["mensagens"] = []
    request.session["mensagens"].append({"texto": mensagem, "tipo": "aviso"})
```

### util/logger_config.py
Deve exportar:
- `logger`: instância configurada de logger

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Criar diretório de logs
Path("logs").mkdir(exist_ok=True)

# Configurar logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Handler para arquivo
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

### util/template_util.py
Deve exportar:
- `criar_templates(pasta)`: função que retorna Jinja2Templates configurado

```python
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

def criar_templates(pasta: str):
    env = Environment(loader=FileSystemLoader(pasta))
    templates = Jinja2Templates(env=env)
    return templates
```

## Configuração de Ambiente

Adicione ao arquivo `.env`:

```env
RUNNING_MODE=Development  # ou Production
```

## Testando o Sistema

Após implementar, teste os seguintes cenários:

1. **Erro 404**: Acesse uma rota que não existe
2. **Erro 401**: Acesse uma rota protegida sem autenticação
3. **Erro 403**: Acesse uma rota sem permissão adequada
4. **Erro de Validação**: Envie dados inválidos em um formulário
5. **Erro 500**: Force uma exceção não tratada no código

Exemplo de teste forçado (adicione temporariamente em uma rota):

```python
@app.get("/test-error")
async def test_error():
    raise Exception("Teste de erro genérico")
```

## Adaptações para Projetos Sem Autenticação

Se o projeto não tiver sistema de autenticação, remova:

1. No handler `http_exception_handler`:
   - Remova os blocos de código para 401 e 403
   - Ou adapte para redirecionar para página inicial

2. No template `404.html`:
   - Remova a verificação de `usuario_logado`
   - Mostre apenas o botão "Ir para Página Inicial"

## Boas Práticas Implementadas

✅ **Separação de Responsabilidades**: Handlers isolados por tipo de exceção
✅ **Logging Apropriado**: Diferentes níveis (debug, warning, error) conforme gravidade
✅ **Segurança**: Não expõe detalhes técnicos em produção
✅ **UX**: Mensagens amigáveis e ações claras para o usuário
✅ **Debug**: Informações detalhadas em desenvolvimento (traceback, request data)
✅ **Performance**: Evita logs desnecessários (arquivos estáticos opcionais)
✅ **Manutenibilidade**: Código bem documentado e organizado

## Notas Finais

- Este sistema funciona para aplicações web com templates Jinja2
- Para APIs JSON, adapte os handlers para retornar `JSONResponse`
- Considere adicionar monitoramento (Sentry, Rollbar) para produção
- Personalize as páginas de erro conforme identidade visual do projeto
- O traceback completo sempre é logado, mesmo em produção
