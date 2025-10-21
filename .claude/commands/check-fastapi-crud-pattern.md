---
description: Verifica se projeto FastAPI segue padrões de CRUD (SQL/Model/Repo/DTO/Routes)
---

# Verificar Padrões de CRUD em Projeto FastAPI

**MODO DE EXECUÇÃO:** Este comando deve ser executado inicialmente em **modo PLAN**.

Analisa um projeto FastAPI e verifica se segue os padrões arquiteturais de CRUD adotados neste projeto (SQL → Model → Repository → DTO → Routes). Gera relatório detalhado de conformidade e oferece correções automáticas.

## Contexto

Este comando verifica conformidade com os seguintes padrões:

### Arquitetura em Camadas

```
Routes (HTTP) → DTOs (Validação) → Repositories (CRUD) → SQL (Queries) → Database
                        ↓
                   Models (Data)
```

### Padrões Esperados

1. **SQL Layer** (`sql/*.py`):
   - Constantes em UPPERCASE (CRIAR_TABELA, INSERIR, etc.)
   - Queries com placeholders `?` (prepared statements)
   - Zero lógica, apenas strings SQL puras
   - Um arquivo por entidade

2. **Model Layer** (`model/*.py`):
   - Python `@dataclass` (não classes normais)
   - Type hints obrigatórios
   - `Optional[]` para campos opcionais
   - Plain Old Data (sem métodos de negócio)
   - Um arquivo por entidade

3. **Repository Layer** (`repo/*.py`):
   - Funções puras (não classes/métodos)
   - Context manager: `with get_connection() as conn:`
   - Import SQL: `from sql.xxx_sql import *`
   - Retorna Models ou primitivos
   - Funções padrão: `criar_tabela()`, `inserir()`, `obter_todos()`, `obter_por_id()`, `atualizar()`, `excluir()`
   - Funções auxiliares privadas com `_` prefix

4. **DTO Layer** (`dtos/*.py`):
   - Pydantic `BaseModel`
   - Validators com `field_validator` decorator
   - Importa validators de `dtos/validators.py`
   - Nomes: `CriarXDTO`, `AlterarXDTO`, `ExcluirXDTO`

5. **Routes Layer** (`routes/*.py`):
   - `APIRouter` com prefix
   - Templates via `criar_templates()` (não `Jinja2Templates`)
   - Decorators: `@requer_autenticacao()`
   - Padrão GET/POST pairs
   - Exception handling: `ValidationError`
   - Flash messages: `informar_sucesso()`, `informar_erro()`
   - PRG Pattern: `RedirectResponse(..., status_code=303)`
   - Logging: `logger.info()`, `logger.warning()`

## FASE 1: Análise do Projeto

### 1.1 Preparação

**IMPORTANTE:** Execute este comando em **modo PLAN**.

```bash
# Claude Code deve estar em modo plan
# Use: /plan antes de executar este comando
```

### 1.2 Identificar Entidades

Primeiro, identifique todas as entidades do projeto:

```bash
# Buscar por models
find . -type f -name "*_model.py" -o -name "*model.py" | grep -v __pycache__

# Buscar por tabelas no banco (se SQLite)
sqlite3 database.db ".tables"

# Buscar por routers
find . -type f -name "*_routes.py" -o -name "*routes.py" | grep -v __pycache__

# Buscar por repositories
find . -type f -name "*_repo.py" -o -name "*repository.py" | grep -v __pycache__
```

Liste todas as entidades encontradas (ex: Usuario, Produto, Pedido, etc.).

### 1.3 Para Cada Entidade, Verificar Camadas

Para cada entidade identificada, execute as verificações abaixo.

## FASE 2: Verificação por Camada

### 2.1 SQL Layer Verification

**Checklist SQL:**

```python
# Arquivo: sql/<entidade>_sql.py

✅ CORRETO:
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
"""

INSERIR = "INSERT INTO produto (nome, preco) VALUES (?, ?)"
OBTER_TODOS = "SELECT * FROM produto ORDER BY nome"
OBTER_POR_ID = "SELECT * FROM produto WHERE id = ?"
ATUALIZAR = "UPDATE produto SET nome = ?, preco = ? WHERE id = ?"
EXCLUIR = "DELETE FROM produto WHERE id = ?"

❌ INCORRETO - String concatenation (SQL Injection):
def inserir(nome):
    return f"INSERT INTO produto (nome) VALUES ('{nome}')"

❌ INCORRETO - Lógica dentro do SQL:
def get_query(tipo):
    if tipo == "ativo":
        return "SELECT * FROM produto WHERE ativo = 1"
    else:
        return "SELECT * FROM produto"

❌ INCORRETO - Classes:
class ProdutoSQL:
    INSERIR = "..."

❌ INCORRETO - Métodos:
def get_insert_query():
    return "INSERT INTO ..."
```

**Verificações:**
1. ✅ Arquivo existe em `sql/<entidade>_sql.py`
2. ✅ Contém constantes: `CRIAR_TABELA`, `INSERIR`, `OBTER_TODOS`, `OBTER_POR_ID`, `ATUALIZAR`, `EXCLUIR`
3. ✅ Usa placeholders `?` (não f-strings ou %)
4. ✅ Apenas strings (não funções ou classes)
5. ✅ Nomes em UPPERCASE

**Comando de verificação:**

```bash
# Verificar se existe
ls -la sql/<entidade>_sql.py

# Verificar padrões
grep -E "(CRIAR_TABELA|INSERIR|OBTER_TODOS|OBTER_POR_ID|ATUALIZAR|EXCLUIR)" sql/<entidade>_sql.py

# Verificar SQL Injection (bad pattern)
grep -E "(f\"|%s|\.format)" sql/<entidade>_sql.py
# Resultado esperado: nenhuma ocorrência

# Verificar placeholders corretos
grep -E "\?" sql/<entidade>_sql.py
# Resultado esperado: múltiplas ocorrências
```

### 2.2 Model Layer Verification

**Checklist Model:**

```python
# Arquivo: model/<entidade>_model.py

✅ CORRETO:
from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: int
    nome: str
    preco: float
    ativo: bool = True
    descricao: Optional[str] = None

❌ INCORRETO - Classe comum:
class Produto:
    def __init__(self, id, nome, preco):
        self.id = id
        self.nome = nome
        self.preco = preco

❌ INCORRETO - Sem type hints:
@dataclass
class Produto:
    id
    nome
    preco

❌ INCORRETO - Métodos de negócio:
@dataclass
class Produto:
    id: int
    nome: str
    preco: float

    def calcular_desconto(self):
        return self.preco * 0.9

❌ INCORRETO - Pydantic BaseModel:
class Produto(BaseModel):  # Isso é DTO, não Model!
    id: int
    nome: str
```

**Verificações:**
1. ✅ Arquivo existe em `model/<entidade>_model.py`
2. ✅ Usa `@dataclass` decorator
3. ✅ Todos os campos têm type hints
4. ✅ Usa `Optional[]` para campos opcionais
5. ✅ Não contém métodos (exceto `__post_init__` se necessário)
6. ✅ Importa de `dataclasses`, não `pydantic`

**Comando de verificação:**

```bash
# Verificar se existe
ls -la model/<entidade>_model.py

# Verificar @dataclass
grep -E "@dataclass" model/<entidade>_model.py

# Verificar imports corretos
grep -E "from dataclasses import" model/<entidade>_model.py

# Verificar se NÃO é Pydantic (anti-pattern)
grep -E "from pydantic import|BaseModel" model/<entidade>_model.py
# Resultado esperado: nenhuma ocorrência

# Verificar type hints
grep -E ":\s*(int|str|float|bool|Optional|datetime)" model/<entidade>_model.py
```

### 2.3 Repository Layer Verification

**Checklist Repository:**

```python
# Arquivo: repo/<entidade>_repo.py

✅ CORRETO:
from typing import Optional
from model.produto_model import Produto
from sql.produto_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(produto: Produto) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (produto.nome, produto.preco))
        return cursor.lastrowid

def obter_todos() -> list[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Produto(
                id=row["id"],
                nome=row["nome"],
                preco=row["preco"]
            )
            for row in rows
        ]

def obter_por_id(id: int) -> Optional[Produto]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Produto(id=row["id"], nome=row["nome"], preco=row["preco"])
        return None

def atualizar(produto: Produto) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (produto.nome, produto.preco, produto.id))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

# Funções auxiliares privadas permitidas
def _converter_row(row) -> Produto:
    return Produto(id=row["id"], nome=row["nome"], preco=row["preco"])

❌ INCORRETO - Classes:
class ProdutoRepository:
    def inserir(self, produto):
        ...

❌ INCORRETO - SQL inline:
def inserir(produto):
    with get_connection() as conn:
        cursor.execute("INSERT INTO produto (nome) VALUES (?)", ...)  # SQL deve estar em sql/*.py

❌ INCORRETO - Sem context manager:
def obter_todos():
    conn = sqlite3.connect("db.db")  # ❌
    cursor = conn.cursor()
    cursor.execute(OBTER_TODOS)
    conn.close()

❌ INCORRETO - Retorna dict ao invés de Model:
def obter_por_id(id):
    ...
    return {"id": row["id"], "nome": row["nome"]}  # ❌ Deve retornar Produto

❌ INCORRETO - Import SQL direto da string:
OBTER_TODOS = "SELECT * FROM produto"  # ❌ Deve importar de sql/*.py
```

**Verificações:**
1. ✅ Arquivo existe em `repo/<entidade>_repo.py`
2. ✅ Importa de `sql.<entidade>_sql import *`
3. ✅ Importa model: `from model.<entidade>_model import <Entidade>`
4. ✅ Importa `get_connection` de `util.db_util`
5. ✅ Usa `with get_connection() as conn:`
6. ✅ Funções (não classes)
7. ✅ Funções padrão existem: `criar_tabela`, `inserir`, `obter_todos`, `obter_por_id`, `atualizar`, `excluir`
8. ✅ Retorna Models ou tipos primitivos (não dicts)
9. ✅ Sem SQL inline (queries vêm de sql/*.py)

**Comando de verificação:**

```bash
# Verificar imports
grep -E "from sql\..* import" repo/<entidade>_repo.py
grep -E "from model\..* import" repo/<entidade>_repo.py
grep -E "from util.db_util import get_connection" repo/<entidade>_repo.py

# Verificar context manager
grep -E "with get_connection\(\) as conn:" repo/<entidade>_repo.py

# Verificar funções padrão
grep -E "^def (criar_tabela|inserir|obter_todos|obter_por_id|atualizar|excluir)" repo/<entidade>_repo.py

# Verificar anti-pattern (classes)
grep -E "^class " repo/<entidade>_repo.py
# Resultado esperado: nenhuma ocorrência

# Verificar anti-pattern (SQL inline)
grep -E "(SELECT|INSERT|UPDATE|DELETE).*(FROM|INTO|SET)" repo/<entidade>_repo.py
# Resultado esperado: apenas em comentários ou strings de variáveis importadas
```

### 2.4 DTO Layer Verification

**Checklist DTOs:**

```python
# Arquivo: dtos/<entidade>_dto.py

✅ CORRETO:
from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria, validar_decimal_positivo

class CriarProdutoDTO(BaseModel):
    nome: str
    preco: float

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_preco = field_validator("preco")(validar_decimal_positivo())

class AlterarProdutoDTO(BaseModel):
    id: int
    nome: str
    preco: float

    _validar_nome = field_validator("nome")(validar_string_obrigatoria("Nome"))
    _validar_preco = field_validator("preco")(validar_decimal_positivo())

❌ INCORRETO - Validação inline:
class CriarProdutoDTO(BaseModel):
    nome: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        if len(v) < 3:  # ❌ Lógica deve estar em validators.py
            raise ValueError("Nome muito curto")
        return v

❌ INCORRETO - Dataclass:
@dataclass  # ❌ DTOs usam Pydantic, não dataclass
class CriarProdutoDTO:
    nome: str

❌ INCORRETO - Sem validators:
class CriarProdutoDTO(BaseModel):
    nome: str  # ❌ Sem validação
    preco: float
```

**Verificações:**
1. ✅ Arquivo existe em `dtos/<entidade>_dto.py`
2. ✅ Usa `BaseModel` do Pydantic
3. ✅ Importa validators de `dtos.validators`
4. ✅ Usa `field_validator` decorator
5. ✅ Nomes seguem padrão: `Criar<Entidade>DTO`, `Alterar<Entidade>DTO`
6. ✅ Validação via funções reutilizáveis (não inline)

**Comando de verificação:**

```bash
# Verificar imports
grep -E "from pydantic import BaseModel" dtos/<entidade>_dto.py
grep -E "from dtos.validators import" dtos/<entidade>_dto.py

# Verificar padrão de nomes
grep -E "class (Criar|Alterar|Excluir).*DTO\(BaseModel\)" dtos/<entidade>_dto.py

# Verificar uso de validators
grep -E "field_validator" dtos/<entidade>_dto.py

# Verificar anti-pattern (validação inline)
grep -E "@field_validator.*\n.*def " dtos/<entidade>_dto.py
# Procurar por métodos de validação customizados (pode ser ok, mas revisar)
```

### 2.5 Routes Layer Verification

**Checklist Routes:**

```python
# Arquivo: routes/<entidade>s_routes.py ou routes/<entidade>_routes.py

✅ CORRETO:
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.produto_dto import CriarProdutoDTO
from model.produto_model import Produto
from repo import produto_repo
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.logger_config import logger

router = APIRouter(prefix="/produtos")
templates = criar_templates("templates/produtos")

@router.get("/listar")
@requer_autenticacao()
async def listar(request: Request, usuario_logado: dict):
    produtos = produto_repo.obter_todos()
    return templates.TemplateResponse(
        "produtos/listar.html",
        {"request": request, "produtos": produtos}
    )

@router.get("/cadastrar")
@requer_autenticacao()
async def get_cadastrar(request: Request, usuario_logado: dict):
    return templates.TemplateResponse("produtos/cadastrar.html", {"request": request})

@router.post("/cadastrar")
@requer_autenticacao()
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    preco: float = Form(...),
    usuario_logado: dict = None
):
    try:
        # Validar com DTO
        dto = CriarProdutoDTO(nome=nome, preco=preco)

        # Criar model
        produto = Produto(id=0, nome=dto.nome, preco=dto.preco)

        # Inserir
        produto_repo.inserir(produto)
        logger.info(f"Produto '{dto.nome}' criado")

        # Flash e redirect
        informar_sucesso(request, "Produto criado com sucesso!")
        return RedirectResponse("/produtos/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = [erro['msg'] for erro in e.errors()]
        informar_erro(request, " | ".join(erros))
        return templates.TemplateResponse(
            "produtos/cadastrar.html",
            {"request": request, "dados": {"nome": nome, "preco": preco}}
        )

❌ INCORRETO - Jinja2Templates direto:
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")  # ❌

❌ INCORRETO - Sem flash messages:
@router.post("/cadastrar")
async def cadastrar(...):
    produto_repo.inserir(produto)
    return RedirectResponse("/produtos")  # ❌ Sem feedback ao usuário

❌ INCORRETO - Status code errado:
return RedirectResponse("/produtos", status_code=302)  # ❌ Deve ser 303

❌ INCORRETO - Sem logging:
# ❌ Nenhum logger.info/warning/error

❌ INCORRETO - Lógica de negócio na rota:
@router.post("/cadastrar")
async def cadastrar(...):
    # ❌ SQL direto
    conn = sqlite3.connect("db.db")
    cursor.execute("INSERT INTO produto ...")

❌ INCORRETO - Sem DTO validation:
@router.post("/cadastrar")
async def cadastrar(nome: str = Form(...)):
    # ❌ Não valida entrada
    produto_repo.inserir(Produto(id=0, nome=nome))
```

**Verificações:**
1. ✅ Arquivo existe em `routes/<entidade>s_routes.py`
2. ✅ Usa `APIRouter` com prefix
3. ✅ Usa `criar_templates()` (não `Jinja2Templates`)
4. ✅ Usa `@requer_autenticacao()` decorator
5. ✅ Padrão GET/POST pairs para formulários
6. ✅ Valida com DTOs e trata `ValidationError`
7. ✅ Usa flash messages: `informar_sucesso()`, `informar_erro()`
8. ✅ Usa `status.HTTP_303_SEE_OTHER` em redirects
9. ✅ Usa logger: `logger.info()`, `logger.warning()`, `logger.error()`
10. ✅ Não contém SQL direto ou lógica de banco

**Comando de verificação:**

```bash
# Verificar imports
grep -E "from util.template_util import criar_templates" routes/<entidade>*_routes.py
grep -E "from util.auth_decorator import requer_autenticacao" routes/<entidade>*_routes.py
grep -E "from util.flash_messages import" routes/<entidade>*_routes.py
grep -E "from util.logger_config import logger" routes/<entidade>*_routes.py

# Verificar APIRouter
grep -E "router = APIRouter\(prefix=" routes/<entidade>*_routes.py

# Verificar uso de templates
grep -E "templates = criar_templates" routes/<entidade>*_routes.py

# Verificar status correto
grep -E "HTTP_303_SEE_OTHER" routes/<entidade>*_routes.py

# Verificar anti-patterns
grep -E "Jinja2Templates\(directory=" routes/<entidade>*_routes.py
# Resultado esperado: nenhuma ocorrência
```

## FASE 3: Geração de Relatório

### 3.1 Estrutura do Relatório

Após analisar todas as entidades, gere um relatório no seguinte formato:

```markdown
# RELATÓRIO DE CONFORMIDADE - PADRÕES DE CRUD

**Projeto:** <nome_do_projeto>
**Data:** <data_atual>
**Entidades Analisadas:** <quantidade>

---

## RESUMO EXECUTIVO

- ✅ **Conformes:** X entidades (Y%)
- ⚠️  **Parcialmente Conformes:** X entidades (Y%)
- ❌ **Não Conformes:** X entidades (Y%)

**Score Geral de Conformidade:** X/100

---

## ANÁLISE POR ENTIDADE

### Entidade: Usuario

#### 1. SQL Layer (`sql/usuario_sql.py`)
- ✅ Arquivo existe
- ✅ Usa constantes UPPERCASE
- ✅ Usa placeholders `?`
- ❌ **PROBLEMA:** Faltam constantes OBTER_TODOS e EXCLUIR
- ⚠️  **AVISO:** Encontrado uso de f-string na linha 45 (risco de SQL injection)

**Score:** 60/100

#### 2. Model Layer (`model/usuario_model.py`)
- ✅ Arquivo existe
- ✅ Usa @dataclass
- ✅ Type hints presentes
- ❌ **PROBLEMA:** Contém método `calcular_idade()` (violar princípio POD)
- ❌ **PROBLEMA:** Campo `email` sem type hint

**Score:** 60/100

#### 3. Repository Layer (`repo/usuario_repo.py`)
- ✅ Arquivo existe
- ✅ Usa funções (não classes)
- ✅ Usa get_connection()
- ❌ **PROBLEMA:** Não importa de sql/usuario_sql.py (SQL inline encontrado)
- ❌ **PROBLEMA:** Função `obter_por_id` retorna dict ao invés de Usuario
- ✅ Funções padrão presentes

**Score:** 50/100

#### 4. DTO Layer (`dtos/usuario_dto.py`)
- ✅ Arquivo existe
- ✅ Usa Pydantic BaseModel
- ❌ **PROBLEMA:** Validação inline (não usa dtos/validators.py)
- ⚠️  **AVISO:** DTO de alteração não valida campos obrigatórios

**Score:** 60/100

#### 5. Routes Layer (`routes/usuarios_routes.py`)
- ✅ Arquivo existe
- ❌ **PROBLEMA:** Usa Jinja2Templates direto (deve usar criar_templates)
- ❌ **PROBLEMA:** Não usa flash messages
- ❌ **PROBLEMA:** Redirect com status 302 (deve ser 303)
- ⚠️  **AVISO:** Sem logging
- ✅ Usa @requer_autenticacao()

**Score:** 40/100

**Score Geral da Entidade Usuario:** 54/100

---

### Entidade: Produto

[Similar structure for each entity]

---

## PROBLEMAS CRÍTICOS ENCONTRADOS

### 🚨 Segurança
1. **SQL Injection Risk** em `sql/usuario_sql.py:45` - uso de f-string
2. **Validação Faltante** em `routes/produtos_routes.py` - entrada não validada

### ⚠️  Arquitetura
1. **SQL Inline** em 3 repositórios (usuario, produto, pedido)
2. **Lógica de Negócio em Model** em `model/usuario_model.py`
3. **Retorno Incorreto** em 2 repos (retornam dict ao invés de Model)

### 🔧 Padrões
1. **Templates** - 5 routes usando Jinja2Templates direto
2. **Flash Messages** - Ausentes em 4 routes
3. **Status HTTP** - 8 redirects usando 302 ao invés de 303
4. **Logging** - Ausente em 90% das routes

---

## PLANO DE CORREÇÃO

### Prioridade ALTA (Segurança)
- [ ] Remover f-strings de SQL (sql/usuario_sql.py:45)
- [ ] Adicionar validação DTO em todas as routes

### Prioridade MÉDIA (Arquitetura)
- [ ] Mover SQL inline para arquivos sql/*.py
- [ ] Remover métodos de negócio dos Models
- [ ] Corrigir retorno de repositórios (dict → Model)

### Prioridade BAIXA (Padrões)
- [ ] Substituir Jinja2Templates por criar_templates()
- [ ] Adicionar flash messages em todas as routes POST
- [ ] Corrigir status HTTP de 302 para 303
- [ ] Adicionar logging em operações CRUD

---

## RECOMENDAÇÕES

1. **Criar arquivo `dtos/validators.py`** com validadores reutilizáveis
2. **Padronizar nomenclatura** de arquivos e funções
3. **Adicionar testes** para garantir conformidade contínua
4. **Documentar padrões** em CONTRIBUTING.md

---

## MÉTRICAS DE QUALIDADE

| Camada       | Conformidade | Problemas Críticos | Avisos |
|--------------|--------------|-------------------|--------|
| SQL          | 70%          | 2                 | 3      |
| Model        | 80%          | 1                 | 2      |
| Repository   | 60%          | 5                 | 1      |
| DTO          | 50%          | 3                 | 4      |
| Routes       | 40%          | 8                 | 12     |
| **TOTAL**    | **60%**      | **19**            | **22** |

---

## PRÓXIMOS PASSOS

Deseja que eu realize as correções automáticas? As seguintes ações serão executadas:

1. ✅ **Automáticas** (Baixo risco):
   - Substituir Jinja2Templates por criar_templates()
   - Corrigir status HTTP 302 → 303
   - Adicionar flash messages básicas
   - Adicionar logging básico
   - Adicionar type hints faltantes

2. ⚠️  **Semi-automáticas** (Requer revisão):
   - Mover SQL inline para arquivos sql/*.py
   - Criar DTOs faltantes
   - Refatorar validação inline → validators.py

3. ❌ **Manuais** (Requer decisão):
   - Remover métodos de Models
   - Reestruturar lógica de negócio
   - Definir estratégia de validação customizada

**Digite 'SIM' para aprovar correções automáticas ou 'REVISAR' para análise detalhada.**
```

### 3.2 Script de Geração Automática

O relatório deve ser gerado executando análise em cada entidade:

```python
# Pseudocódigo da análise

def analisar_projeto():
    entidades = descobrir_entidades()
    relatorio = {
        "entidades": [],
        "problemas": [],
        "score_geral": 0
    }

    for entidade in entidades:
        analise = {
            "nome": entidade,
            "sql": verificar_sql_layer(entidade),
            "model": verificar_model_layer(entidade),
            "repo": verificar_repo_layer(entidade),
            "dto": verificar_dto_layer(entidade),
            "routes": verificar_routes_layer(entidade)
        }

        relatorio["entidades"].append(analise)

    gerar_relatorio_markdown(relatorio)
    perguntar_usuario_acoes()
```

## FASE 4: Correções Automáticas

### 4.1 Correções de Baixo Risco (Automáticas)

**1. Substituir Jinja2Templates:**

```python
# Buscar e substituir
rg "Jinja2Templates\(directory=" --files-with-matches | while read file; do
    # Adicionar import
    sed -i '1i from util.template_util import criar_templates' "$file"

    # Substituir uso
    sed -i 's/Jinja2Templates(directory="templates"/criar_templates("templates/g' "$file"
    sed -i 's/Jinja2Templates(directory="templates\(.*\)"/criar_templates("templates\1/g' "$file"
done
```

**2. Corrigir Status HTTP:**

```python
# Substituir 302 por 303
rg "status_code=302" --files-with-matches | while read file; do
    sed -i 's/status_code=302/status_code=status.HTTP_303_SEE_OTHER/g' "$file"
done
```

**3. Adicionar Flash Messages:**

Detectar routes POST sem flash messages e adicionar template básico.

### 4.2 Correções Semi-Automáticas

**1. Mover SQL Inline para Arquivos:**

Detectar SQL inline em repos e sugerir migração:

```python
# Detectar
rg "(SELECT|INSERT|UPDATE|DELETE)" repo/*.py -A 2 -B 2

# Para cada ocorrência, extrair e criar em sql/*.py
```

**2. Criar DTOs Faltantes:**

Analisar routes que recebem Form(...) sem DTO e gerar template.

### 4.3 Correções Manuais (Sugestões)

Listar problemas que requerem decisão humana com sugestões de como resolver.

## FASE 5: Validação Pós-Correção

Após realizar correções, re-executar análise e comparar scores:

```
ANTES  → DEPOIS
SQL:    70% → 95%
Model:  80% → 90%
Repo:   60% → 85%
DTO:    50% → 80%
Routes: 40% → 90%
TOTAL:  60% → 88%
```

## Uso do Comando

```bash
# 1. Entrar em modo plan
/plan

# 2. Executar comando
/check-fastapi-crud-pattern

# 3. Aguardar análise

# 4. Revisar relatório

# 5. Aprovar correções
# Digite: SIM (correções automáticas) ou REVISAR (análise detalhada)

# 6. Sair do modo plan (após correções)
/exec
```

## Checklist de Verificação Manual

Após executar comando, revisar manualmente:

- [ ] Todas as queries SQL usam placeholders `?`
- [ ] Nenhum Model contém lógica de negócio
- [ ] Repositories retornam Models (não dicts)
- [ ] DTOs validam todas as entradas
- [ ] Routes usam flash messages
- [ ] Logging presente em operações críticas
- [ ] Status HTTP 303 em redirects POST
- [ ] Nenhum SQL inline nos repositórios

## Limitações Conhecidas

1. **ORMs não suportados:** Este padrão é para SQL puro (não SQLAlchemy/Tortoise)
2. **APIs JSON:** Padrão otimizado para templates (adaptar para APIs)
3. **Validação customizada:** Pode requerer ajustes manuais
4. **Migrações:** Não cobre sistema de migrations

## Conclusão

Este comando fornece análise abrangente de conformidade com padrões de CRUD e oferece correções automáticas para a maioria dos problemas detectados, garantindo consistência arquitetural no projeto.
