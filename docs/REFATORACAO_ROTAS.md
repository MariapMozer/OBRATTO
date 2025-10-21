# Guia de Refatoração: routes/publico/publico_routes.py

## Problema Identificado

O arquivo `routes/publico/publico_routes.py` contém **1.234 linhas** com **31 endpoints**, tornando-o difícil de manter e navegar.

## Estrutura Recomendada

Dividir o arquivo em módulos menores por funcionalidade:

```
routes/publico/
├── __init__.py                 # Exporta o router principal
├── home_routes.py              # Endpoints da home/index
├── produto_routes.py           # Endpoints de produtos públicos
├── servico_routes.py           # Endpoints de serviços públicos
├── fornecedor_routes.py        # Endpoints de fornecedores públicos
├── prestador_routes.py         # Endpoints de prestadores públicos
├── auth_routes.py              # Login, logout, registro, recuperação de senha
└── contato_routes.py           # Formulário de contato, sobre, etc.
```

## Padrão de Implementação

### Exemplo 1: home_routes.py

```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from util.templates import obter_jinja_templates

router = APIRouter(tags=["Home Pública"])
templates = obter_jinja_templates("templates")


@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    \"\"\"Página inicial do site\"\"\"
    return templates.TemplateResponse(
        "publico/home.html",
        {"request": request}
    )


@router.get("/sobre", response_class=HTMLResponse)
async def get_sobre(request: Request):
    \"\"\"Página sobre a plataforma\"\"\"
    return templates.TemplateResponse(
        "publico/sobre.html",
        {"request": request}
    )
```

### Exemplo 2: auth_routes.py

```python
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from util.templates import obter_jinja_templates
from data.usuario import usuario_repo
from util.security import verificar_senha, criar_hash_senha

router = APIRouter(tags=["Autenticação Pública"])
templates = obter_jinja_templates("templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    \"\"\"Exibe formulário de login\"\"\"
    return templates.TemplateResponse(
        "publico/login.html",
        {"request": request}
    )


@router.post("/login")
async def post_login(request: Request, email: str = Form(...), senha: str = Form(...)):
    \"\"\"Processa login do usuário\"\"\"
    # ... lógica de login
    pass


@router.get("/logout")
async def get_logout(request: Request):
    \"\"\"Faz logout do usuário\"\"\"
    request.session.clear()
    return RedirectResponse("/", status_code=303)
```

### Exemplo 3: produto_routes.py

```python
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from util.templates import obter_jinja_templates
from data.produto import produto_repo

router = APIRouter(tags=["Produtos Públicos"], prefix="/produtos")
templates = obter_jinja_templates("templates")


@router.get("/", response_class=HTMLResponse)
async def listar_produtos(
    request: Request,
    pagina: int = Query(1, ge=1),
    busca: Optional[str] = None
):
    \"\"\"Lista produtos disponíveis\"\"\"
    produtos = produto_repo.obter_produto_por_pagina(
        limit=12,
        offset=(pagina - 1) * 12
    )
    return templates.TemplateResponse(
        "publico/produtos.html",
        {
            "request": request,
            "produtos": produtos,
            "pagina": pagina
        }
    )


@router.get("/{produto_id}", response_class=HTMLResponse)
async def detalhe_produto(request: Request, produto_id: int):
    \"\"\"Exibe detalhes de um produto\"\"\"
    produto = produto_repo.obter_produto_por_id(produto_id)
    return templates.TemplateResponse(
        "publico/produto_detalhe.html",
        {
            "request": request,
            "produto": produto
        }
    )
```

## Como Consolidar no __init__.py

```python
# routes/publico/__init__.py
from fastapi import APIRouter
from . import (
    home_routes,
    auth_routes,
    produto_routes,
    servico_routes,
    fornecedor_routes,
    prestador_routes,
    contato_routes,
)

# Router principal que consolida todos os subrouters
router = APIRouter()

# Incluir todos os subrouters
router.include_router(home_routes.router)
router.include_router(auth_routes.router)
router.include_router(produto_routes.router)
router.include_router(servico_routes.router)
router.include_router(fornecedor_routes.router)
router.include_router(prestador_routes.router)
router.include_router(contato_routes.router)
```

## Benefícios da Refatoração

1. **Manutenibilidade**: Arquivos menores (100-200 linhas) são mais fáceis de entender
2. **Organização**: Funcionalidades relacionadas ficam juntas
3. **Colaboração**: Múltiplos desenvolvedores podem trabalhar sem conflitos
4. **Testabilidade**: Mais fácil testar rotas específicas isoladamente
5. **Performance do IDE**: Editores carregam mais rápido com arquivos menores

## Passos para Refatorar

1. **Identificar grupos de rotas** relacionadas
2. **Criar novo arquivo** para cada grupo (ex: `produto_routes.py`)
3. **Mover rotas** do arquivo original para o novo
4. **Mover imports** necessários junto com as rotas
5. **Testar** cada módulo individualmente
6. **Atualizar** o `__init__.py` para incluir o novo router
7. **Atualizar** `main.py` para usar o novo sistema modular
8. **Remover** código duplicado/obsoleto

## Estimativa de Esforço

- **Tempo estimado**: 2-3 horas
- **Complexidade**: Média
- **Risco**: Baixo (refatoração não altera funcionalidade)
- **Prioridade**: Média (melhoria de qualidade de código)

## Notas para Implementação Futura

- Considere criar uma classe base para rotas públicas se houver muita lógica comum
- Implemente testes para cada módulo de rotas separadamente
- Documente cada endpoint com docstrings adequadas
- Use tags do FastAPI para organizar a documentação automática (Swagger)
