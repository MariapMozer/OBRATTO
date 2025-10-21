# Guia de Setup - OBRATTO

Este guia fornece instruções passo a passo para configurar e executar o projeto OBRATTO em sua máquina local.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Execução](#execução)
5. [Testes](#testes)
6. [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- **Python 3.11+** ([Download Python](https://www.python.org/downloads/))
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

### Verificar instalação

```bash
python3 --version  # Deve retornar 3.11 ou superior
pip --version      # Deve retornar a versão do pip
git --version      # Deve retornar a versão do git
```

---

## Instalação

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd OBRATTO
```

### 2. Criar ambiente virtual

É **altamente recomendado** usar um ambiente virtual para isolar as dependências:

```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
# No macOS/Linux:
source .venv/bin/activate

# No Windows:
.venv\Scripts\activate
```

Quando o ambiente virtual estiver ativo, você verá `(.venv)` no início do prompt.

### 3. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuração

### 1. Criar arquivo de configuração

Copie o arquivo de exemplo para criar sua configuração local:

```bash
cp .env.example .env
```

### 2. Configurar SECRET_KEY

A SECRET_KEY é **obrigatória** para o funcionamento da aplicação. Gere uma chave segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Abra o arquivo `.env` e adicione a chave gerada:

```env
SECRET_KEY=<sua-chave-secreta-gerada>
```

### 3. Configurações opcionais

O arquivo `.env` permite outras configurações opcionais:

```env
# Banco de dados (padrão: obratto.db)
DATABASE_PATH=obratto.db

# Banco de dados para testes (padrão: test_obratto.db)
TEST_DATABASE_PATH=test_obratto.db

# Tempo de expiração da sessão em segundos (padrão: 3600 = 1 hora)
SESSION_MAX_AGE=3600

# Nome da aplicação (padrão: OBRATTO)
APP_NAME=OBRATTO

# Versão (padrão: 1.0.0)
VERSION=1.0.0

# Modo debug (padrão: False)
DEBUG=False
```

### 4. Inicializar o banco de dados

O banco de dados SQLite será criado automaticamente na primeira execução. Para popular com dados iniciais:

```bash
python -m util.seed_db
```

Este comando criará usuários padrão para teste:

| Tipo          | Email                     | Senha      |
|---------------|---------------------------|------------|
| Admin         | admin@obratto.com         | admin123   |
| Cliente       | cliente@obratto.com       | cliente123 |
| Fornecedor    | fornecedor@obratto.com    | fornec123  |
| Prestador     | prestador@obratto.com     | presta123  |

---

## Execução

### Modo desenvolvimento

Execute a aplicação em modo desenvolvimento com hot reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em: **http://localhost:8000**

### Modo produção

Para executar em modo produção (sem hot reload):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Acessar a aplicação

Abra seu navegador e acesse:

- **Home**: http://localhost:8000
- **Login**: http://localhost:8000/login
- **Escolher tipo de cadastro**: http://localhost:8000/escolha_cadastro

---

## Testes

### Executar todos os testes

```bash
pytest
```

### Executar testes com cobertura

```bash
pytest --cov=. --cov-report=html
```

O relatório HTML será gerado em `htmlcov/index.html`

### Executar testes específicos

```bash
# Testar apenas auth_routes
pytest tests/test_auth_routes.py -v

# Testar apenas um teste específico
pytest tests/test_auth_routes.py::TestLoginRoutes::test_login_sucesso_cliente -v
```

### Executar testes com output detalhado

```bash
pytest -v --tb=short
```

---

## Estrutura do Projeto

```
OBRATTO/
├── main.py                     # Ponto de entrada da aplicação
├── requirements.txt            # Dependências do projeto
├── .env.example               # Template de configuração
├── .env                       # Configuração local (não commitado)
├── .gitignore                 # Arquivos ignorados pelo git
├── data/                      # Camada de dados
│   ├── cliente/
│   ├── fornecedor/
│   ├── prestador/
│   ├── produto/
│   └── usuario/
├── dtos/                      # Data Transfer Objects (validação)
│   ├── cliente/
│   ├── fornecedor/
│   └── produto/
├── routes/                    # Rotas da aplicação
│   ├── publico/              # Rotas públicas (sem autenticação)
│   ├── cliente/
│   ├── fornecedor/
│   ├── prestador/
│   └── administrador/
├── templates/                 # Templates HTML (Jinja2)
│   ├── publico/
│   ├── cliente/
│   └── ...
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── img/
├── util/                      # Utilitários
│   ├── auth_decorator.py     # Autenticação e rate limiting
│   ├── db.py                 # Conexão com banco de dados
│   ├── security.py           # Funções de segurança
│   └── ...
└── tests/                     # Testes automatizados
    ├── conftest.py           # Configuração dos testes
    ├── test_auth_routes.py   # Testes de autenticação
    └── ...
```

---

## Recursos Implementados

### Segurança

✅ **Rate Limiting**
- Login: 5 tentativas por 5 minutos (por IP)
- Cadastro: 3 tentativas por hora (por IP)

✅ **Autenticação**
- Hash de senha com bcrypt
- Sessões seguras com SessionMiddleware
- Proteção contra timing attacks

✅ **Validação**
- Validação MIME type de imagens (magic numbers)
- Validação de CPF/CNPJ
- DTOs com Pydantic para validação de dados

### Funcionalidades

✅ **Autenticação**
- Login/Logout
- Recuperação de senha
- Redefinição de senha

✅ **Cadastro**
- Cliente
- Fornecedor
- Prestador

✅ **Perfis de usuário**
- Admin
- Cliente
- Fornecedor
- Prestador

### Melhorias Recentes

✅ **Refatoração de rotas**
- Separação em módulos específicos
- Melhor organização do código

✅ **Testes**
- 17 testes para rotas de autenticação
- Cobertura de login, logout, recuperação de senha

✅ **Documentação**
- Docstrings detalhados em todas as rotas
- Guia de setup completo

---

## Troubleshooting

### Erro: "SECRET_KEY não configurada"

**Solução**: Configure a SECRET_KEY no arquivo `.env`

```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Cole a chave gerada no arquivo .env
```

### Erro: "ModuleNotFoundError"

**Solução**: Certifique-se de que o ambiente virtual está ativo e as dependências instaladas

```bash
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Erro: "Address already in use"

**Solução**: A porta 8000 já está em uso. Use outra porta ou encerre o processo:

```bash
# Usar outra porta
uvicorn main:app --reload --port 8001

# Ou encontrar e encerrar o processo na porta 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
```

### Testes falhando

**Solução**: Certifique-se de que o banco de dados de teste está limpo

```bash
rm -f test_obratto.db
pytest
```

### Erro: "OperationalError: database is locked"

**Solução**: Feche outras conexões com o banco de dados

```bash
# No código, certifique-se de usar connection pooling
# Ou reinicie a aplicação
```

---

## Comandos Úteis

### Desenvolvimento

```bash
# Verificar código com flake8
flake8 .

# Formatar código com black
black .

# Executar mypy para type checking
python3 -m mypy .

# Ver logs da aplicação
tail -f logs/obratto.log
```

### Banco de dados

```bash
# Acessar o banco SQLite
sqlite3 obratto.db

# Listar tabelas
sqlite3 obratto.db ".tables"

# Ver schema de uma tabela
sqlite3 obratto.db ".schema usuario"

# Backup do banco
cp obratto.db obratto_backup_$(date +%Y%m%d).db
```

### Git

```bash
# Ver status
git status

# Ver commits recentes
git log --oneline -10

# Criar nova branch
git checkout -b feature/minha-feature

# Commit com mensagem
git add .
git commit -m "Descrição das mudanças"
```

---

## Próximos Passos

Após configurar o projeto, você pode:

1. ✅ Explorar a aplicação em http://localhost:8000
2. ✅ Fazer login com os usuários de teste
3. ✅ Criar novos cadastros
4. ✅ Explorar as diferentes áreas por perfil
5. ✅ Executar e estudar os testes
6. ✅ Contribuir com novas funcionalidades

---

## Suporte

Para dúvidas ou problemas:

1. Consulte este guia de setup
2. Verifique a seção [Troubleshooting](#troubleshooting)
3. Revise os logs da aplicação
4. Abra uma issue no repositório

---

**Versão do Guia**: 1.0.0
**Última atualização**: 2025-10-21
**Projeto**: OBRATTO - Plataforma de Construção Civil
