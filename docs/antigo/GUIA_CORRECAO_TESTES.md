# 🔧 GUIA RÁPIDO DE CORREÇÃO DE TESTES

## 🎯 Objetivo
Este guia mostra como corrigir rapidamente os testes falhando no projeto OBRATTO.

---

## ✅ CORREÇÕES JÁ APLICADAS

### 1. Fixtures de Dados Únicos
Adicionadas no `tests/conftest.py`:
- `email_unico` - Gera email único
- `cpf_unico` - Gera CPF válido único
- `dados_usuario_unico` - Dicionário completo com dados únicos

### 2. DTOs Corrigidos
- Removidos imports inexistentes
- Adicionado import `datetime` nos testes

---

## 🚀 COMO USAR AS FIXTURES

### Exemplo 1: Email Único

**ANTES (Causava erro):**
```python
def test_inserir_cliente(self, test_db):
    usuario = Usuario(email="teste@email.com", ...)  # ❌ Email duplicado
    cliente_repo.inserir(usuario)
```

**DEPOIS (Correto):**
```python
def test_inserir_cliente(self, test_db, email_unico):
    usuario = Usuario(email=email_unico, ...)  # ✅ Email único
    cliente_repo.inserir(usuario)
```

### Exemplo 2: Dados Completos Únicos

**ANTES:**
```python
def test_inserir_fornecedor(self, test_db):
    usuario = Usuario(
        email="teste@email.com",
        cpf_cnpj="12345678901",
        nome="Teste",
        senha="123",
        # ... muitos campos ...
    )
```

**DEPOIS:**
```python
def test_inserir_fornecedor(self, test_db, dados_usuario_unico):
    # Personalizar apenas o que precisa
    dados_usuario_unico["tipo_usuario"] = "fornecedor"
    usuario = Usuario(**dados_usuario_unico)
```

---

## 🔧 CORREÇÕES RÁPIDAS POR ARQUIVO

### test_cliente_repo.py

#### Correção 1: Email Único
```python
# Adicionar parâmetro email_unico nas funções de teste
def test_inserir_cliente(self, test_db, email_unico):
    usuario = Usuario(
        id=0,
        email=email_unico,  # ✅ Mudança aqui
        # ... resto dos campos
    )
```

#### Correção 2: Row.get() Issue
```python
# Linha 76 - Trocar:
campo = row.get("nome", "")

# Por:
campo = row["nome"] if "nome" in row.keys() else ""
```

---

### test_fornecedor_repo.py

**Aplicar mesma correção de email único:**

```python
# Adicionar aos testes:
def test_inserir_fornecedor(self, test_db, email_unico):
    # Usar email_unico ao invés de email fixo
```

---

### test_prestador_repo.py

**Aplicar mesma correção de email único + CPF único:**

```python
def test_inserir_prestador(self, test_db, email_unico, cpf_unico):
    usuario = Usuario(
        email=email_unico,
        cpf_cnpj=cpf_unico,
        # ... resto
    )
```

---

### test_servico_repo.py

**Aplicar correção de email único:**

```python
# Testes que criam usuários devem usar email_unico
```

---

### test_anuncio_repo.py

**Aplicar correção de email único:**

```python
# Testes que criam fornecedores devem usar email_unico
```

---

## 📝 CHECKLIST DE CORREÇÃO

Para cada teste que falha com "UNIQUE constraint failed":

- [ ] Adicionar `email_unico` aos parâmetros da função de teste
- [ ] Substituir email fixo por `email_unico`
- [ ] Se usar CPF/CNPJ, adicionar `cpf_unico` e usá-lo
- [ ] Rodar o teste novamente: `pytest tests/test_arquivo.py -v`

---

## 🎬 EXEMPLO COMPLETO DE CORREÇÃO

### Antes (Test Falhando)
```python
class TestClienteRepo:
    def test_inserir_cliente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()

        usuario = Usuario(
            id=0,
            nome="Cliente Teste",
            email="cliente@teste.com",  # ❌ Problema aqui
            senha="senha123",
            cpf_cnpj="12345678901",     # ❌ Problema aqui
            telefone="27999999999",
            cep="29100-000",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro",
            cidade="Cidade",
            estado="ES",
            tipo_usuario="cliente",
            data_cadastro=datetime.now().isoformat()
        )

        id_usuario = inserir_usuario(usuario)
        cliente = Cliente(id_cliente=id_usuario)
        inserir_cliente(cliente)
        # ... resto do teste
```

### Depois (Test Passando)
```python
class TestClienteRepo:
    def test_inserir_cliente(self, test_db, email_unico, cpf_unico):
        criar_tabela_usuario()
        criar_tabela_cliente()

        usuario = Usuario(
            id=0,
            nome="Cliente Teste",
            email=email_unico,          # ✅ Corrigido
            senha="senha123",
            cpf_cnpj=cpf_unico,          # ✅ Corrigido
            telefone="27999999999",
            cep="29100-000",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro",
            cidade="Cidade",
            estado="ES",
            tipo_usuario="cliente",
            data_cadastro=datetime.now().isoformat()
        )

        id_usuario = inserir_usuario(usuario)
        cliente = Cliente(id_cliente=id_usuario)
        inserir_cliente(cliente)
        # ... resto do teste
```

---

## 🏃 ORDEM DE EXECUÇÃO RECOMENDADA

1. **Dia 1: Correções Simples (2-3h)**
   - Corrigir test_cliente_repo.py
   - Corrigir test_fornecedor_repo.py
   - Corrigir test_prestador_repo.py
   - **Meta:** +17 testes passando

2. **Dia 2: Correções Médias (3-4h)**
   - Corrigir test_servico_repo.py
   - Corrigir test_anuncio_repo.py
   - Investigar erros de schema SQL
   - **Meta:** +10 testes passando

3. **Dia 3: Correções Avançadas (4-5h)**
   - Corrigir erros de schema em administrador_repo
   - Criar fixtures de autenticação
   - Corrigir testes de routes
   - **Meta:** +15 testes passando

---

## 🧪 COMANDOS ÚTEIS

```bash
# Rodar teste específico
pytest tests/test_cliente_repo.py::TestClienteRepo::test_inserir_cliente -v

# Rodar todos os testes de um arquivo
pytest tests/test_cliente_repo.py -v

# Rodar com mais detalhes de erro
pytest tests/test_cliente_repo.py -vv --tb=long

# Rodar apenas testes que falharam
pytest tests/test_cliente_repo.py --lf -v

# Rodar e parar no primeiro erro
pytest tests/test_cliente_repo.py -x -v

# Ver apenas resumo
pytest tests/ --tb=no -q
```

---

## ✅ VALIDAÇÃO

Após cada correção, validar com:

```bash
# 1. Rodar o teste corrigido
pytest tests/test_arquivo.py -v

# 2. Verificar que passou
# ✅ PASSED = Sucesso!
# ❌ FAILED = Precisa mais correção

# 3. Commit se passou
git add tests/test_arquivo.py
git commit -m "fix: corrigir testes de [entidade]"
```

---

## 📈 META FINAL

**Situação Atual:** 54/123 testes passando (44%)

**Meta Dia 1:** 71/123 (58%)
**Meta Dia 2:** 81/123 (66%)
**Meta Dia 3:** 96/123 (78%)
**Meta Final:** 120/123 (98%)

---

## 💡 DICAS

1. **Sempre use email_unico:** Para qualquer teste que cria usuário
2. **Use dados_usuario_unico:** Quando precisar de um usuário completo
3. **Rode um teste por vez:** Mais fácil debugar
4. **Commit após cada arquivo:** Não perca seu progresso
5. **Documente problemas:** Se encontrar bug no código, anote

---

## 🆘 PROBLEMAS COMUNS

### Problema: "UNIQUE constraint failed"
**Solução:** Adicionar fixture `email_unico` ou `cpf_unico`

### Problema: "no such column"
**Solução:** Verificar schema do banco e corrigir query SQL

### Problema: "Row object has no attribute 'get'"
**Solução:** Usar `row["campo"]` ao invés de `row.get("campo")`

### Problema: "Test retorna página de login"
**Solução:** Criar fixture de autenticação (ver RELATORIO_CORRECAO_TESTES.md)

---

## 📞 PRÓXIMOS PASSOS

1. Ler `docs/RELATORIO_CORRECAO_TESTES.md` para detalhes completos
2. Começar pelas correções mais simples (email_unico)
3. Testar incrementalmente
4. Documentar problemas encontrados

**Boa sorte! 🚀**
