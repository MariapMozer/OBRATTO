# 🎓 PLANO DE CORREÇÃO E PREPARAÇÃO DO PROJETO OBRATTO

**Professor:** [Seu nome]
**Disciplina:** Engenharia de Software / Projeto Integrador
**Objetivo:** Preparar projeto de referência com infraestrutura completa + marcações TODO para os alunos
**Data de Criação:** 20 de Outubro de 2025

---

## 📋 RESUMO EXECUTIVO

Este plano visa transformar o projeto OBRATTO em uma **base pedagógica sólida** onde:

1. **Infraestrutura funciona 100%** (auth, logger, exceptions, toasts, repos)
2. **Rotas públicas estão completas** (cadastro, login, home)
3. **Banco de dados está populado** (usuários de teste com fotos)
4. **Funcionalidades dos alunos têm marcações TODO** (guias para correção)
5. **Testes de repositórios passam** (garantia de qualidade)

**Tempo estimado:** 6-8 horas
**Abordagem:** Incremental e testada a cada fase

---

## 🎯 FASES DE EXECUÇÃO

### **FASE 1: Auditoria e Documentação (1h)**

**Objetivo:** Mapear o estado atual e criar baseline

#### 1.1 Verificar Status da Infraestrutura

- [ ] Testar sistema de autenticação/autorização
- [ ] Validar exception handlers (404, 500, 401, 403)
- [ ] Confirmar sistema de toasts funcionando
- [ ] Verificar logging (rotação, níveis)
- [ ] Rodar todos os testes: `pytest tests/ -v`

**Critério de sucesso:** Documentar % de testes passando e funcionalidades OK

#### 1.2 Mapear Inconsistências das Rotas

- [ ] Identificar rotas com DTOs ✅ vs sem DTOs ❌
- [ ] Listar funções vazias ou `pass`
- [ ] Documentar valores hardcoded
- [ ] Mapear código comentado (dead code)

**Entregável:** Arquivo `docs/AUDITORIA_INICIAL.md`

---

### **FASE 2: Correção da Infraestrutura Base (2h)**

**Objetivo:** Garantir que fundações estão 100% sólidas

#### 2.1 Sistema de Logging

- [ ] Criar `util/logger_setup.py` (logger unificado)
- [ ] Substituir todos `print()` por `logger.info/error`
- [ ] Configurar níveis: DEBUG (dev), INFO (prod)
- [ ] Testar rotação de logs (10MB máx)

**Código exemplo:**

```python
# util/logger_setup.py
import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    TODO ALUNOS: Entender como funciona o sistema de logging centralizado
    - Por que usar RotatingFileHandler?
    - Qual a diferença entre DEBUG, INFO, WARNING, ERROR?
    """
    logger = logging.getLogger(name)
    # ... configuração
    return logger
```

#### 2.2 Validações e DTOs

- [ ] Revisar DTOs existentes (publico, administrador, produto)
- [ ] **NÃO criar DTOs** para rotas de alunos (deixar como TODO)
- [ ] Adicionar validadores Pydantic em `util/validacoes_dto.py`
- [ ] Documentar padrão de validação

**Exemplo de marcação:**

```python
# routes/cliente/cliente_perfil.py

# TODO ALUNOS: Implementar validação com DTO
# 1. Criar dtos/cliente/atualizar_cliente_dto.py
# 2. Importar: from dtos.cliente.atualizar_cliente_dto import AtualizarClienteDTO
# 3. Validar dados antes de persistir
# 4. Referência: publico_routes.py linhas 103-121 (CriarPrestadorDTO)
# 5. Consultar: docs/DTO.md
@router.post("/editar/dados")
async def processar_edicao_perfil_cliente(...):
    pass  # TODO: Implementar validação e atualização
```

#### 2.3 Flash Messages Padronizado

- [ ] Garantir `util/flash_messages.py` funcional
- [ ] Testar em template base: `{% if messages %}`
- [ ] **NÃO corrigir** rotas dos alunos (marcar TODO)

**Exemplo de marcação:**

```python
# TODO ALUNOS: Padronizar feedback ao usuário
# Substituir: return RedirectResponse(f"/perfil?erro=...")
# Por: informar_erro(request, "Mensagem de erro clara")
# Referência: fornecedor_produtos.py linha 124
# Documentação: docs/SISTEMA_TOASTS.md
```

---

### **FASE 3: Preparação do Banco de Dados (1.5h)**

**Objetivo:** Criar ambiente realista para testes

#### 3.1 Script de População

- [ ] Criar `scripts/popular_banco.py`
- [ ] Gerar usuários para TODOS os perfis:
  - 3 administradores
  - 5 clientes (diferentes gêneros, idades)
  - 5 prestadores (áreas variadas)
  - 5 fornecedores (com produtos)

**Estrutura do script:**

```python
#!/usr/bin/env python3
"""
Script de população do banco de dados para ambiente de desenvolvimento

TODO ALUNOS: Entender o fluxo de criação de usuários
1. Por que usamos DTOs para validação antes de inserir?
2. Como as senhas são protegidas (hash)?
3. Por que criar usuários de teste é importante?

Uso: python scripts/popular_banco.py
"""
import sys
sys.path.append('.')
from util.security import criar_hash_senha
from data.cliente import cliente_repo
# ...

def criar_clientes_teste():
    """Cria 5 clientes com perfis diversos"""
    clientes = [
        {
            "nome": "Maria Silva",
            "email": "maria.silva@teste.com",
            "senha": "Senha@123",  # Hash será criado
            "genero": "Feminino",
            "data_nascimento": date(1990, 5, 15),
            # ...
        },
        # ... mais 4 clientes
    ]
    for dados in clientes:
        # Validação com DTO
        # Criação do objeto
        # Inserção no banco
        pass

if __name__ == "__main__":
    print("🌱 Populando banco de dados...")
    criar_clientes_teste()
    criar_prestadores_teste()
    criar_fornecedores_teste()
    criar_administradores_teste()
    print("✅ Banco populado com sucesso!")
```

#### 3.2 Fotos de Teste

- [ ] Baixar imagens de perfil de teste (unsplash/pexels - licença livre)
- [ ] Criar `static/uploads/teste/` com fotos
- [ ] Script move fotos para diretórios corretos
- [ ] Garantir permissões de escrita

**Estrutura:**

```
static/uploads/
  ├── teste/              # Fotos originais
  │   ├── cliente_1.jpg
  │   ├── prestador_1.jpg
  │   └── fornecedor_1.jpg
  ├── cliente/            # Copiadas pelo script
  ├── prestador/
  └── fornecedor/
```

#### 3.3 Dados Relacionados

- [ ] Criar produtos para cada fornecedor (3-5 produtos)
- [ ] Criar serviços para cada prestador (2-4 serviços)
- [ ] Criar planos (básico, padrão, premium)
- [ ] Criar algumas avaliações (notas 3-5)

**Objetivo pedagógico:** Alunos terão dados realistas para testar funcionalidades

---

### **FASE 4: Rotas Públicas 100% Funcionais (1.5h)**

**Objetivo:** Garantir que cadastro e login funcionam perfeitamente

#### 4.1 Rota de Cadastro (Prestador, Cliente, Fornecedor)

- [ ] Testar `POST /cadastro/prestador`
- [ ] Testar `POST /cadastro/cliente`
- [ ] Testar `POST /cadastro/fornecedor`
- [ ] Validar:
  - DTOs funcionando
  - Upload de foto
  - Flash messages
  - Redirect para login
  - Email duplicado bloqueado

**Checklist de validação:**

```python
# TODO ALUNOS: Fluxo completo de cadastro
# ✅ 1. Formulário HTML envia dados via POST
# ✅ 2. Dados validados por DTO (CriarClienteDTO)
# ✅ 3. Senha transformada em hash (nunca salve senha pura!)
# ✅ 4. Email verificado (duplicidade)
# ✅ 5. Objeto criado (Cliente, Prestador, Fornecedor)
# ✅ 6. Persistido no banco via Repository
# ✅ 7. Flash message de sucesso
# ✅ 8. Redirect para /login
#
# Teste manual:
# 1. Acesse: http://localhost:8000/cadastro/cliente
# 2. Preencha o formulário
# 3. Verifique se aparece "Cadastro realizado com sucesso!"
# 4. Tente fazer login com as credenciais
```

#### 4.2 Rota de Login

- [ ] Testar `POST /login`
- [ ] Validar:
  - Autenticação com senha hash
  - Criação de sessão
  - Redirect por perfil (admin→/administrador, cliente→/cliente, etc)
  - Rate limiting funcionando

**Teste de segurança:**

```python
# TODO ALUNOS: Segurança no login
# ✅ 1. Senha NUNCA é comparada em texto puro
# ✅ 2. Usamos verificar_senha(senha_digitada, senha_hash_banco)
# ✅ 3. Rate limiting: máx 5 tentativas/minuto
# ✅ 4. Logging de tentativas falhas
# ✅ 5. Mensagem genérica: "Email ou senha inválidos"
#
# Teste manual:
# 1. Tente logar 6 vezes com senha errada
# 2. Verifique se bloqueia temporariamente
# 3. Verifique logs: logs/obratto.log
```

#### 4.3 Rota Home Pública

- [ ] Testar `GET /`
- [ ] Garantir que carrega sem autenticação
- [ ] Links para cadastro/login funcionais

---

### **FASE 5: Marcação TODO nas Rotas dos Alunos (2h)**

**Objetivo:** Criar guia pedagógico inline no código

#### 5.1 Padrão de Marcação

Criar arquivo `docs/GUIA_MARCACOES_TODO.md`:

```markdown
# Guia de Marcações TODO para Alunos

## Tipos de TODO

### 🔴 TODO CRÍTICO: Funcionalidade não implementada

Indica código vazio ou bugado que DEVE ser corrigido.

### 🟡 TODO MELHORIA: Funcionalidade parcial

Indica código que funciona mas pode ser melhorado.

### 🔵 TODO ESTUDO: Ponto de aprendizado

Indica conceito importante para entender.

## Estrutura de um TODO

```python
# TODO [TIPO]: [O QUE FAZER]
# [POR QUÊ]
# Passos:
# 1. [Passo 1]
# 2. [Passo 2]
# Referência: [arquivo:linha ou doc]
# Documentação: [caminho do doc]
# Critério de sucesso: [como testar]
```

## Exemplos Práticos

### Função Vazia

```python
# TODO CRÍTICO: Implementar edição de perfil do cliente
# Esta função está vazia e não salva alterações no banco.
# Passos:
# 1. Criar DTO: dtos/cliente/atualizar_cliente_dto.py
# 2. Validar dados com o DTO
# 3. Buscar cliente no banco: cliente_repo.obter_cliente_por_id()
# 4. Atualizar atributos do objeto Cliente
# 5. Persistir: cliente_repo.atualizar_cliente(cliente)
# 6. Adicionar flash message de sucesso
# 7. Redirecionar para /cliente/perfil
# Referência: publico_routes.py linha 228 (cadastro completo)
# Documentação: docs/DTO.md, docs/RELATORIO_CONFORMIDADE_CRUD.md
# Critério de sucesso: Alterar nome do cliente e verificar mudança no banco
@router.post("/editar/dados")
async def processar_edicao_perfil_cliente(...):
    pass
```

### Validação Ausente

```python
# TODO MELHORIA: Adicionar validação com DTO
# Atualmente aceita qualquer valor, pode gerar erros de dados.
# Passos:
# 1. Criar dtos/prestador/atualizar_prestador_dto.py
# 2. Copiar estrutura de CriarPrestadorDTO
# 3. Remover campos imutáveis (id, data_cadastro)
# 4. Adicionar validação: dados_dto = AtualizarPrestadorDTO(...)
# 5. Tratar ValidationError
# Referência: publico_routes.py linhas 181-204
# Documentação: docs/DTO.md seção "Validação com Pydantic"
# Critério de sucesso: Tentar enviar email inválido e ver mensagem de erro clara
```

### Logging Ausente

```python
# TODO ESTUDO: Entender importância do logging
# Print não persiste informações e dificulta debug em produção.
# Passos:
# 1. Importar: from util.logger_setup import get_logger
# 2. Criar logger: logger = get_logger(__name__)
# 3. Substituir: print(f"Erro: {e}") → logger.error(f"Erro ao...: {e}")
# 4. Usar níveis apropriados:
#    - logger.info() → ações importantes (login, cadastro)
#    - logger.warning() → situações anormais (email duplicado)
#    - logger.error() → erros que precisam atenção
# Referência: administrador_usuarios.py linha 70
# Documentação: docs/SISTEMA_AUTENTICACAO.md seção "Logging"
# Critério de sucesso: Executar ação e ver entrada em logs/obratto.log
```

```
```

#### 5.2 Aplicar Marcações nos Arquivos

**cliente_perfil.py:**

- [ ] Função `processar_edicao_perfil_cliente` (linha 64)
- [ ] Adicionar TODO sobre DTO
- [ ] Adicionar TODO sobre logging

**prestador_perfil.py:**

- [ ] Função `processar_edicao_perfil_prestador` (linha 73)
- [ ] Adicionar TODO sobre implementação completa

**prestador_servicos.py:**

- [ ] Remover código comentado (linhas 172-196)
- [ ] Substituir `print` por TODO sobre logging

**fornecedor_perfil.py:**

- [ ] Adicionar TODO sobre imports duplicados
- [ ] Adicionar TODO sobre DTO

**fornecedor_planos.py:**

- [ ] Adicionar TODO sobre valores hardcoded
- [ ] Explicar como usar `usuario_logado["id"]`

**avaliacao.py:**

- [ ] Adicionar TODO sobre autenticação ausente
- [ ] Adicionar TODO sobre DTO
- [ ] Adicionar TODO sobre camada de serviço

#### 5.3 Criar Arquivo de Checklist

Criar `docs/CHECKLIST_ALUNOS.md`:

```markdown
# 📝 Checklist de Correções para os Alunos

## Como usar este checklist

1. Cada item corresponde a um TODO no código
2. Marque com ✅ quando concluir
3. Teste ANTES de marcar como concluído
4. Consulte a documentação linkada em cada item

## 🔴 Crítico (Funcionalidades Não Implementadas)

### Cliente

- [ ] `routes/cliente/cliente_perfil.py:64` - Implementar edição de perfil
  - **Arquivo:** cliente_perfil.py
  - **Função:** processar_edicao_perfil_cliente
  - **O que fazer:** Validar com DTO e salvar no banco
  - **Como testar:** Alterar nome e verificar mudança
  - **Doc:** docs/DTO.md

### Prestador

- [ ] `routes/prestador/prestador_perfil.py:73` - Implementar edição de perfil
- [ ] `routes/prestador/prestador_servicos.py:77` - Substituir print por logging

### Fornecedor

- [ ] `routes/fornecedor/fornecedor_planos.py:42` - Remover id_fornecedor hardcoded

### Avaliação

- [ ] `routes/avaliacao/avaliacao.py` - Adicionar autenticação
- [ ] `routes/avaliacao/avaliacao.py` - Criar DTOs de validação

## 🟡 Melhorias (Funcionalidades Parciais)

### Geral

- [ ] Padronizar flash messages em todas as rotas
- [ ] Adicionar logging estruturado em todas as operações CRUD
- [ ] Remover código comentado (dead code)

## 🔵 Estudo (Pontos de Aprendizado)

- [ ] Entender fluxo completo de autenticação
- [ ] Compreender validação com Pydantic
- [ ] Aprender diferença entre print e logging
- [ ] Estudar padrão Repository

## 📊 Progresso

**Total de TODOs:** [SERÁ PREENCHIDO AUTOMATICAMENTE]
**Concluídos:** 0
**Porcentagem:** 0%

---

**Dica:** Use `grep -r "TODO" routes/` para listar todos os TODOs
```

---

### **FASE 6: Revisão e Testes Finais (1h)**

**Objetivo:** Garantir que tudo funciona antes da entrega

#### 6.1 Testes de Repositórios

- [ ] Rodar: `pytest tests/ -v --tb=short`
- [ ] Corrigir apenas testes de repos usados em rotas públicas
- [ ] **NÃO corrigir** testes de funcionalidades dos alunos
- [ ] Atingir pelo menos 80% de testes passando nos repos críticos

**Repos críticos (devem passar 100%):**

- `test_cliente_repo.py`
- `test_prestador_repo.py`
- `test_fornecedor_repo.py`
- `test_administrador_repo.py`
- `test_usuario_repo.py`

#### 6.2 Testes Manuais E2E

Criar script de teste manual: `docs/ROTEIRO_TESTE_ENTREGA.md`

```markdown
# Roteiro de Teste para Entrega aos Alunos

## Preparação

1. Limpar banco: `python scripts/limpar_banco.py`
2. Popular: `python scripts/popular_banco.py`
3. Iniciar servidor: `uvicorn main:app --reload`

## Fluxo 1: Cadastro de Cliente

1. Acesse: http://localhost:8000/cadastro/cliente
2. Preencha todos os campos
3. Upload de foto (JPG < 5MB)
4. Clique em "Cadastrar"
5. ✅ Deve aparecer: "Cadastro realizado com sucesso!"
6. ✅ Deve redirecionar para: /login

## Fluxo 2: Login como Cliente

1. Acesse: http://localhost:8000/login
2. Use: cliente1@teste.com / Senha@123
3. ✅ Deve redirecionar para: /cliente
4. ✅ Deve mostrar nome do usuário no header
5. ✅ Foto de perfil deve aparecer

## Fluxo 3: Login como Prestador

1. Logout
2. Login com: prestador1@teste.com / Senha@123
3. ✅ Deve redirecionar para: /prestador
4. ✅ Menu lateral deve ter opções de prestador

## Fluxo 4: Login como Fornecedor

1. Logout
2. Login com: fornecedor1@teste.com / Senha@123
3. ✅ Deve redirecionar para: /fornecedor
4. ✅ Deve listar produtos cadastrados

## Fluxo 5: Login como Administrador

1. Logout
2. Login com: admin@obratto.com / Admin@123
3. ✅ Deve redirecionar para: /administrador/home
4. ✅ Deve ter acesso a painéis de moderação

## Fluxo 6: Testar Páginas de Erro

1. Acesse: http://localhost:8000/pagina-inexistente
2. ✅ Deve mostrar página 404 personalizada
3. Logout e tente acessar: /cliente
4. ✅ Deve redirecionar para /login com mensagem

## Fluxo 7: Verificar Logging

1. Execute ações acima
2. Verifique: `tail -f logs/obratto.log`
3. ✅ Deve ter logs de: login, cadastro, erros

## Critérios de Aprovação

- [ ] Todos os fluxos 1-7 funcionam
- [ ] 0 erros no console do navegador
- [ ] 0 erros fatais no terminal (uvicorn)
- [ ] Banco populado com 18 usuários
- [ ] Fotos de perfil carregando
```

#### 6.3 Documentação Final

- [ ] Atualizar `README.md` principal
- [ ] Criar `docs/PARA_OS_ALUNOS.md` com instruções
- [ ] Listar todas as melhorias feitas
- [ ] Listar todos os TODOs criados

**Exemplo `docs/PARA_OS_ALUNOS.md`:**

```markdown
# 🎓 Orientações para os Alunos - Projeto OBRATTO

Queridos alunos,

Este projeto foi preparado com a **infraestrutura de software completa e funcional**.

## ✅ O que está pronto e funcionando

### 1. Autenticação e Autorização

- ✅ Sistema de login com sessão
- ✅ Proteção de rotas por perfil
- ✅ Validação de senha forte
- ✅ Rate limiting (proteção contra brute force)
- **Documentação:** `docs/SISTEMA_AUTENTICACAO.md`

### 2. Tratamento de Exceções

- ✅ Páginas de erro personalizadas (404, 500)
- ✅ Logging automático de erros
- ✅ Redirecionamento seguro
- **Documentação:** `docs/EXCEPTION_HANDLERS_README.md`

### 3. Sistema de Notificações

- ✅ Toasts Bootstrap 5
- ✅ Flash messages integradas
- ✅ 4 tipos: sucesso, erro, aviso, info
- **Documentação:** `docs/SISTEMA_TOASTS.md`

### 4. Logging Profissional

- ✅ Logs rotativos (10MB máx)
- ✅ Níveis: DEBUG, INFO, WARNING, ERROR
- ✅ Arquivo: `logs/obratto.log`
- **Como usar:** `docs/SISTEMA_AUTENTICACAO.md` seção "Logging"

### 5. Validação com DTOs

- ✅ Pydantic para validação de entrada
- ✅ Mensagens de erro claras
- ✅ Exemplos em rotas públicas
- **Documentação:** `docs/DTO.md`

### 6. Banco de Dados Populado

- ✅ 3 administradores
- ✅ 5 clientes
- ✅ 5 prestadores
- ✅ 5 fornecedores
- ✅ Produtos, serviços, planos
- **Credenciais:** Veja `scripts/popular_banco.py`

## 📝 O que vocês precisam fazer

Todas as tarefas estão marcadas com `TODO` no código.

### Como encontrar os TODOs

```bash
# Listar todos os TODOs
grep -r "TODO" routes/

# Contar TODOs por arquivo
grep -r "TODO" routes/ | cut -d: -f1 | sort | uniq -c
```

### Tipos de TODO

- **TODO CRÍTICO:** Funcionalidade não implementada (deve corrigir)
- **TODO MELHORIA:** Funcionalidade parcial (pode melhorar)
- **TODO ESTUDO:** Ponto de aprendizado (deve entender)

### Checklist Completo

Consulte: `docs/CHECKLIST_ALUNOS.md`

## 🧪 Como Testar

1. **Testes Automáticos:**

```bash
pytest tests/ -v
```

2. **Testes Manuais:**
   Siga: `docs/ROTEIRO_TESTE_ENTREGA.md`

## 📚 Documentação Disponível

| Documento                              | Conteúdo                      |
| -------------------------------------- | ----------------------------- |
| `docs/DTO.md`                          | Validação com Pydantic        |
| `docs/SISTEMA_AUTENTICACAO.md`         | Auth completo                 |
| `docs/SISTEMA_TOASTS.md`               | Notificações                  |
| `docs/EXCEPTION_HANDLERS_README.md`    | Erros                         |
| `docs/RELATORIO_CONFORMIDADE_CRUD.md`  | Padrões CRUD                  |
| `docs/GUIA_MARCACOES_TODO.md`          | Como corrigir TODOs           |

## ❓ Dúvidas Frequentes

### Como criar um DTO?

Consulte `docs/DTO.md` seção "Criando um Novo DTO"

### Como adicionar logging?

Veja exemplo em `routes/publico/publico_routes.py:34`

### Como usar flash messages?

Veja exemplo em `routes/fornecedor/fornecedor_produtos.py:159`

## 🎯 Critérios de Avaliação

Seu trabalho será avaliado por:

1. ✅ Todos os TODOs CRÍTICOS corrigidos
2. ✅ Testes de repositórios passando (100%)
3. ✅ Código seguindo padrões do projeto
4. ✅ Documentação inline (docstrings)
5. ✅ Funcionalidades testadas manualmente

## 💡 Dicas

1. **Leia PRIMEIRO a documentação** antes de codificar
2. **Copie e adapte** código das rotas públicas (já estão corretas)
3. **Teste SEMPRE** após cada mudança
4. **Commit FREQUENTE** (use git)
5. **Peça ajuda** quando travar (mas tente primeiro!)

---

**Boa sorte!** 🚀

Professor [Seu nome]
```

---

## 📦 ENTREGÁVEIS FINAIS

### Código

1. ✅ Infraestrutura 100% funcional
2. ✅ Rotas públicas completas
3. ✅ TODOs pedagógicos inline
4. ✅ Testes de repos críticos passando (>80%)
5. ✅ Banco de dados populado

### Documentação

1. ✅ `docs/PARA_OS_ALUNOS.md` - Guia principal
2. ✅ `docs/CHECKLIST_ALUNOS.md` - Lista de tarefas
3. ✅ `docs/GUIA_MARCACOES_TODO.md` - Como corrigir
4. ✅ `docs/ROTEIRO_TESTE_ENTREGA.md` - Como testar
5. ✅ `docs/AUDITORIA_INICIAL.md` - Estado inicial

### Scripts

1. ✅ `scripts/popular_banco.py` - População de dados
2. ✅ `scripts/limpar_banco.py` - Limpeza para reset
3. ✅ `scripts/validar_entrega.py` - Validação automática

---

## 🔍 VALIDAÇÃO FINAL

Antes de entregar aos alunos, executar:

```bash
# 1. Limpar e popular banco
python scripts/limpar_banco.py
python scripts/popular_banco.py

# 2. Rodar testes
pytest tests/ -v --tb=short

# 3. Validar rotas públicas
python scripts/validar_entrega.py

# 4. Testar manualmente
# Seguir: docs/ROTEIRO_TESTE_ENTREGA.md

# 5. Contar TODOs
grep -r "TODO" routes/ | wc -l
```

**Critérios de aprovação:**

- [ ] Testes repos críticos: 100% passando
- [ ] Rotas públicas: 100% funcionais
- [ ] Banco: 18 usuários + dados relacionados
- [ ] TODOs: 25-35 marcações pedagógicas
- [ ] Docs: 5 arquivos novos criados
- [ ] Zero erros fatais ao iniciar servidor

---

## 📅 CRONOGRAMA SUGERIDO

| Fase                  | Tempo | Quando fazer  |
| --------------------- | ----- | ------------- |
| 1 - Auditoria         | 1h    | Dia 1 manhã   |
| 2 - Infraestrutura    | 2h    | Dia 1 tarde   |
| 3 - Banco de dados    | 1.5h  | Dia 2 manhã   |
| 4 - Rotas públicas    | 1.5h  | Dia 2 tarde   |
| 5 - Marcações TODO    | 2h    | Dia 3 manhã   |
| 6 - Testes finais     | 1h    | Dia 3 tarde   |

**Total:** 9 horas distribuídas em 3 dias

---

## 📞 OBSERVAÇÕES PEDAGÓGICAS

### Por que deixar TODOs em vez de corrigir tudo?

1. **Aprendizado ativo:** Alunos aprendem FAZENDO, não só lendo
2. **Código de referência:** Rotas públicas servem de exemplo
3. **Guia inline:** TODOs explicam O QUÊ e COMO fazer
4. **Autonomia gradual:** Começa com TODOs detalhados, avança para mais complexos
5. **Avaliação justa:** Você tem baseline do que era problema original

### Filosofia de Correção

- ✅ **Corrigir:** Infraestrutura (base sólida)
- ✅ **Exemplificar:** Rotas públicas (referência)
- ❌ **NÃO corrigir:** Funcionalidades dos alunos
- ✅ **Guiar:** TODOs pedagógicos detalhados

### Diferencial Pedagógico

Este não é um projeto "pronto" entregue aos alunos.
É um projeto **estruturado para aprendizado progressivo**:

1. Infraestrutura sólida (não perdem tempo com bugs de base)
2. Exemplos funcionais (têm referência de código bom)
3. Guias inline (sabem O QUE e COMO fazer)
4. Autonomia preservada (ainda precisam FAZER)
5. Validação objetiva (testes como critério de sucesso)

---

## 📊 MÉTRICAS DE SUCESSO

### Quantitativas

- [ ] **Testes:** >80% passando nos repos críticos
- [ ] **Cobertura:** Infraestrutura 100% funcional
- [ ] **TODOs:** 25-35 marcações pedagógicas
- [ ] **Documentação:** 5+ novos arquivos .md
- [ ] **Usuários teste:** 18 no banco
- [ ] **Tempo execução:** <10 horas

### Qualitativas

- [ ] **Clareza:** TODOs são auto-explicativos
- [ ] **Didática:** Código de referência é exemplar
- [ ] **Realismo:** Banco tem dados variados e realistas
- [ ] **Usabilidade:** Rotas públicas funcionam perfeitamente
- [ ] **Profissionalismo:** Logs, erros, toasts integrados

---

## 🚦 STATUS DO PROJETO

**Estado Atual:** ⏸️ Aguardando início da execução
**Última atualização:** 20 de Outubro de 2025
**Próxima fase:** FASE 1 - Auditoria e Documentação

---

**✍️ Notas do Professor:**

[Espaço reservado para anotações durante a execução do plano]

---

**📞 Suporte:**

- Dúvidas técnicas: Consultar documentação em `docs/`
- Problemas no plano: Revisar este arquivo
- Ajustes necessários: Documentar na seção "Notas do Professor"
