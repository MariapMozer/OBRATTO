# 🧪 Roteiro de Testes de Entrega - Projeto OBRATTO

Este documento fornece um roteiro completo de testes para validar o sistema antes da entrega.

**Tempo estimado**: 30-40 minutos

---

## 📋 Pré-requisitos

Antes de começar os testes, certifique-se de que:

```bash
# 1. Banco de dados está populado
python scripts/limpar_banco.py     # Digite SIM
python scripts/migrar_schema.py
python scripts/popular_banco.py
python scripts/gerar_fotos_teste.py

# 2. Testes automatizados passando
python -m pytest tests/ -v
# Deve mostrar: 122 passed

# 3. Servidor iniciado
uvicorn main:app --reload
# Aguarde: "Application startup complete"
```

---

## ✅ PARTE 1: Testes Automatizados (5 min)

### 1.1 Rodar Todos os Testes

```bash
python -m pytest tests/ -v
```

**Resultado esperado:**
```
======================== 122 passed in X.XXs ==========================
```

**Se algum teste falhar:**
1. Leia a mensagem de erro
2. Identifique qual arquivo/função falhou
3. Corrija o problema
4. Rode novamente

### 1.2 Testar Cobertura (Opcional)

```bash
python -m pytest tests/ --cov=routes --cov=data --cov-report=html
```

Abra `htmlcov/index.html` no navegador para ver cobertura detalhada.

---

## ✅ PARTE 2: Rotas Públicas (10 min)

### 2.1 Página Home

**URL**: http://localhost:8000/

**Checklist:**
- [ ] Página carrega sem erros
- [ ] Layout Bootstrap está correto
- [ ] Links de navegação funcionam
- [ ] Botão "Login" está visível
- [ ] Botão "Cadastrar" está visível
- [ ] Não há erros no console do navegador

**Teste de flash messages** (se houver):
- [ ] Mensagens aparecem como toasts
- [ ] Desaparecem automaticamente após 5s
- [ ] Podem ser fechadas manualmente

---

### 2.2 Página de Login

**URL**: http://localhost:8000/login

**Checklist:**
- [ ] Formulário de login aparece
- [ ] Campos: Email e Senha
- [ ] Botão "Entrar" funciona
- [ ] Link "Esqueci minha senha" existe
- [ ] Link "Cadastrar" redireciona corretamente

**Teste de Login Válido:**

**Credenciais**: `admin@obratto.com` / `Senha@123`

**Passos:**
1. Digite email: `admin@obratto.com`
2. Digite senha: `Senha@123`
3. Clique em "Entrar"

**Resultado esperado:**
- [ ] Redirecionou para dashboard do admin
- [ ] Nome do usuário aparece no header
- [ ] Flash message de boas-vindas aparece
- [ ] Menu de navegação específico do admin visível

**Teste de Login Inválido:**

**Credenciais**: `teste@erro.com` / `senhaerrada`

**Passos:**
1. Digite email inválido
2. Digite senha incorreta
3. Clique em "Entrar"

**Resultado esperado:**
- [ ] Permanece na página de login
- [ ] Flash message de erro aparece
- [ ] Mensagem: "Credenciais inválidas" ou similar

---

### 2.3 Escolha de Cadastro

**URL**: http://localhost:8000/escolha_cadastro

**Checklist:**
- [ ] Página carrega
- [ ] 3 opções visíveis: Cliente, Prestador, Fornecedor
- [ ] Cada opção tem descrição clara
- [ ] Botões redirecionam para formulário correto

---

### 2.4 Cadastro de Cliente

**URL**: http://localhost:8000/cadastro/cliente

**Checklist - Interface:**
- [ ] Formulário completo aparece
- [ ] Campos obrigatórios marcados com *
- [ ] Máscaras de entrada funcionam (CPF, telefone, CEP)
- [ ] Campo de senha tem toggle para mostrar/ocultar
- [ ] Campo "Confirmar Senha" existe

**Teste de Cadastro Válido:**

**Dados de teste:**
```
Nome: João Teste Silva
Email: joao.teste@example.com
CPF: 123.456.789-00
Telefone: (27) 99999-9999
Gênero: Masculino
Data de Nascimento: 01/01/1995
CEP: 29000-000
Estado: ES
Cidade: Vitória
Rua: Rua Teste
Número: 123
Bairro: Centro
Senha: Teste@123
Confirmar Senha: Teste@123
```

**Passos:**
1. Preencha todos os campos
2. Clique em "Cadastrar"

**Resultado esperado:**
- [ ] Redirecionou para /login
- [ ] Flash message de sucesso aparece
- [ ] Pode fazer login com as credenciais criadas

**Teste de Validação (DTO):**

**Cenário 1 - Email inválido:**
- Email: `emailinvalido`
- **Esperado**: Mensagem de erro "Email inválido"

**Cenário 2 - Senhas não conferem:**
- Senha: `Teste@123`
- Confirmar: `Teste@456`
- **Esperado**: Mensagem "Senhas não conferem"

**Cenário 3 - Campos obrigatórios vazios:**
- Deixe nome em branco
- **Esperado**: Mensagem "Campo obrigatório"

---

### 2.5 Cadastro de Prestador

**URL**: http://localhost:8000/cadastro/prestador

**Checklist adicional (além dos campos de cliente):**
- [ ] Campo "Área de Atuação" (dropdown)
- [ ] Campo "Razão Social"
- [ ] Campo "Descrição de Serviços" (textarea)

**Dados de teste:**
```
[Mesmos campos do cliente +]
Área de Atuação: Elétrica
Razão Social: João Serviços Elétricos MEI
Descrição: Instalações e manutenção elétrica residencial
```

**Resultado esperado:**
- [ ] Cadastro bem-sucedido
- [ ] Pode fazer login como prestador

---

### 2.6 Cadastro de Fornecedor

**URL**: http://localhost:8000/cadastro/fornecedor

**Checklist:**
- [ ] Usa CNPJ em vez de CPF
- [ ] Campo "Razão Social" obrigatório
- [ ] Sem campos de gênero/data nascimento

**Dados de teste:**
```
Nome: Loja Teste Materiais
Email: loja.teste@example.com
CNPJ: 12.345.678/0001-90
Telefone: (27) 3333-0000
Razão Social: Loja Teste Materiais de Construção Ltda
[... outros campos ...]
```

**Resultado esperado:**
- [ ] Cadastro bem-sucedido
- [ ] Pode fazer login como fornecedor

---

## ✅ PARTE 3: Fluxos de Usuário (15 min)

### 3.1 Fluxo do Cliente

**Login**: `maria.silva@teste.com` / `Senha@123`

**Checklist:**
1. **Dashboard/Perfil**
   - [ ] Nome do cliente aparece
   - [ ] Email exibido corretamente
   - [ ] Foto de perfil (placeholder) aparece
   - [ ] Menu de navegação específico do cliente

2. **Buscar Serviços** (se implementado)
   - [ ] Pode buscar prestadores
   - [ ] Filtros funcionam
   - [ ] Pode ver perfil do prestador

3. **Solicitar Orçamento** (se implementado)
   - [ ] Formulário de solicitação funciona
   - [ ] Flash message confirma envio

4. **Editar Perfil**
   - [ ] GET /cliente/perfil/editar carrega formulário
   - [ ] Dados atuais pré-preenchidos
   - [ ] **SE IMPLEMENTADO**: POST atualiza dados
   - [ ] **SE IMPLEMENTADO**: Flash message de sucesso
   - [ ] **SE NÃO IMPLEMENTADO**: Função tem TODO ALUNO

5. **Logout**
   - [ ] Link de logout funciona
   - [ ] Redireciona para /login
   - [ ] Sessão foi encerrada

---

### 3.2 Fluxo do Prestador

**Login**: `pedro.eletricista@teste.com` / `Senha@123`

**Checklist:**
1. **Dashboard**
   - [ ] Nome e área de atuação aparecem
   - [ ] Estatísticas visíveis (se houver)
   - [ ] Menu específico de prestador

2. **Gerenciar Serviços** (se implementado)
   - [ ] Lista de serviços carrega
   - [ ] Pode criar novo serviço
   - [ ] Pode editar serviço
   - [ ] Pode excluir serviço

3. **Responder Orçamentos** (se implementado)
   - [ ] Lista de solicitações aparece
   - [ ] Pode visualizar detalhes
   - [ ] Pode enviar proposta

4. **Editar Perfil**
   - [ ] GET /prestador/perfil/editar carrega
   - [ ] Campos específicos: área_atuacao, razao_social, descricao_servicos
   - [ ] **SE IMPLEMENTADO**: POST funciona
   - [ ] **SE NÃO IMPLEMENTADO**: Tem TODO ALUNO

---

### 3.3 Fluxo do Fornecedor

**Login**: `contato@casadastintas.com` / `Senha@123`

**Checklist:**
1. **Dashboard**
   - [ ] Razão social aparece
   - [ ] Menu específico de fornecedor

2. **Gerenciar Produtos**
   - [ ] GET /fornecedor/produtos lista produtos
   - [ ] Produtos do banco aparecem (3 produtos de tintas)
   - [ ] Pode criar novo produto
   - [ ] Pode editar produto
   - [ ] Pode excluir produto
   - [ ] Upload de foto funciona

3. **Editar Perfil**
   - [ ] Formulário de edição funciona
   - [ ] Pode atualizar razão social

---

### 3.4 Fluxo do Administrador

**Login**: `admin@obratto.com` / `Senha@123`

**Checklist:**
1. **Dashboard Admin**
   - [ ] Painel de controle aparece
   - [ ] Estatísticas do sistema (se houver)

2. **Gerenciar Usuários**
   - [ ] GET /administrador/usuarios lista todos os usuários
   - [ ] Tabela paginada (se houver)
   - [ ] Pode ver detalhes de usuário
   - [ ] Pode bloquear/desbloquear usuário
   - [ ] Pode alterar tipo de usuário

3. **Gerenciar Anúncios** (se implementado)
   - [ ] Lista de anúncios
   - [ ] Pode aprovar/rejeitar
   - [ ] Pode excluir

4. **Logs do Sistema** (se implementado)
   - [ ] Pode visualizar logs
   - [ ] Filtros funcionam

---

## ✅ PARTE 4: Validações de Segurança (5 min)

### 4.1 Teste de Autenticação

**Cenário 1 - Acesso sem login:**

**Teste:**
1. Faça logout (se estiver logado)
2. Tente acessar: http://localhost:8000/cliente/perfil

**Resultado esperado:**
- [ ] Redireciona para /login
- [ ] Flash message: "Você precisa estar logado"

**Cenário 2 - Acesso com perfil errado:**

**Teste:**
1. Login como cliente: `maria.silva@teste.com`
2. Tente acessar: http://localhost:8000/prestador/perfil

**Resultado esperado:**
- [ ] Retorna erro 403 (Forbidden)
- [ ] Ou redireciona para página de erro
- [ ] NÃO permite acesso

---

### 4.2 Teste de Autorização

**Teste:**
1. Login como cliente
2. Tente acessar: http://localhost:8000/administrador/usuarios

**Resultado esperado:**
- [ ] Acesso negado (403)
- [ ] Cliente NÃO vê lista de usuários

---

### 4.3 Validação de Senhas

**Checklist:**
- [ ] Senhas são armazenadas com hash (não plain text)
- [ ] Login falha com senha incorreta
- [ ] Não é possível ver senha de outros usuários

**Verificação no banco:**
```bash
sqlite3 obratto.db "SELECT email, senha FROM usuario LIMIT 3;"
```

**Resultado esperado:**
- Senhas aparecem como hashes (ex: `$2b$12$...`)
- NÃO aparecem como "Senha@123"

---

## ✅ PARTE 5: Funcionalidades Complementares (5 min)

### 5.1 Flash Messages / Toasts

**Teste:**
1. Faça login
2. Faça logout
3. Tente cadastro com email duplicado

**Checklist:**
- [ ] Mensagens aparecem como toasts do Bootstrap
- [ ] Cores corretas: sucesso (verde), erro (vermelho), info (azul)
- [ ] Auto-desaparecem após 5s
- [ ] Podem ser fechadas com X

---

### 5.2 Sistema de Logging

**Verificar arquivo de log:**
```bash
ls -lh logs/
cat logs/app.log | tail -50
```

**Checklist:**
- [ ] Arquivo `logs/app.log` existe
- [ ] Contém timestamps
- [ ] Registra logins
- [ ] Registra erros
- [ ] Formato: `[NIVEL] data hora - mensagem`

**Exemplo esperado:**
```
[INFO] 2025-10-20 10:30:15 - OBRATTO v1.0.0 iniciando...
[INFO] 2025-10-20 10:30:16 - SessionMiddleware configurado
[INFO] 2025-10-20 10:32:45 - Login bem-sucedido: maria.silva@teste.com
```

---

### 5.3 Exception Handlers

**Teste 404 - Página não encontrada:**

**URL**: http://localhost:8000/pagina-inexistente

**Resultado esperado:**
- [ ] Retorna status 404
- [ ] Exibe página de erro amigável
- [ ] Ou redireciona para home
- [ ] Log registra o erro 404

**Teste 500 - Erro interno:**

Esse teste pode não ser aplicável se não houver erro forçado no código.

---

## ✅ PARTE 6: Banco de Dados (5 min)

### 6.1 Verificar Dados Populados

```bash
sqlite3 obratto.db
```

**Queries de verificação:**
```sql
-- Contar usuários por tipo
SELECT tipo_usuario, COUNT(*) FROM usuario GROUP BY tipo_usuario;
-- Esperado: Cliente(5), Prestador(5), Fornecedor(5), Administrador(3)

-- Contar produtos
SELECT COUNT(*) FROM produto;
-- Esperado: 15

-- Contar planos
SELECT COUNT(*) FROM plano;
-- Esperado: 3

-- Verificar integridade: produtos sem fornecedor
SELECT COUNT(*) FROM produto WHERE fornecedor_id NOT IN (SELECT id FROM fornecedor);
-- Esperado: 0

.quit
```

**Checklist:**
- [ ] 18 usuários no total
- [ ] 15 produtos
- [ ] 3 planos
- [ ] Sem registros órfãos

---

### 6.2 Verificar Foreign Keys

```bash
sqlite3 obratto.db "PRAGMA foreign_keys = ON; PRAGMA foreign_key_check;"
```

**Resultado esperado:**
- Sem output (nenhuma violação de FK)

---

## ✅ PARTE 7: Scripts de Manutenção (5 min)

### 7.1 Script de População

```bash
python scripts/popular_banco.py
```

**Checklist:**
- [ ] Executa sem erros
- [ ] Exibe mensagens de progresso
- [ ] Exibe resumo final
- [ ] Mostra total de usuários/produtos/planos criados

### 7.2 Script de Limpeza

```bash
python scripts/limpar_banco.py
# (NÃO digite SIM - apenas teste que funciona)
```

**Checklist:**
- [ ] Pede confirmação
- [ ] Aceita apenas "SIM" maiúsculo
- [ ] Mostra aviso de que é destrutivo

### 7.3 Script de Migração

```bash
python scripts/migrar_schema.py
```

**Checklist:**
- [ ] Executa sem erros
- [ ] Informa se há migrações pendentes
- [ ] Pode ser executado múltiplas vezes sem erro

### 7.4 Script de Fotos

```bash
python scripts/gerar_fotos_teste.py
```

**Checklist:**
- [ ] Gera 18 fotos de usuários
- [ ] Gera 15 fotos de produtos
- [ ] Salva em `static/uploads/teste/`

---

## 📊 Resumo Final

### Checklist de Entrega

**Infraestrutura:**
- [ ] Todos os 122 testes passam
- [ ] Servidor inicia sem erros
- [ ] Sem erros no console

**Funcionalidades Públicas:**
- [ ] Home carrega corretamente
- [ ] Login funciona (todos os perfis)
- [ ] Cadastros funcionam (cliente, prestador, fornecedor)
- [ ] Flash messages aparecem

**Autenticação/Autorização:**
- [ ] Rotas protegidas exigem login
- [ ] Autorização por perfil funciona
- [ ] Senhas com hash

**Sistema:**
- [ ] Logger gravando em arquivo
- [ ] Exception handlers funcionando
- [ ] Banco populado corretamente

**Scripts:**
- [ ] popular_banco.py funcional
- [ ] limpar_banco.py funcional
- [ ] migrar_schema.py funcional
- [ ] gerar_fotos_teste.py funcional

**Documentação:**
- [ ] README.md atualizado
- [ ] docs/CREDENCIAIS_TESTE.md criado
- [ ] docs/PARA_OS_ALUNOS.md criado
- [ ] docs/ROTEIRO_TESTE_ENTREGA.md criado

**TODOs Pedagógicos:**
- [ ] Cliente perfil edição marcado
- [ ] Prestador perfil edição marcado
- [ ] Código comentado marcado
- [ ] print() vs logger marcado

---

## 🎯 Critérios de Aprovação

### ✅ Sistema PRONTO para entrega se:

1. **Todos os 122 testes passam** (obrigatório)
2. **Rotas públicas 100% funcionais**:
   - Home, Login, Cadastros
3. **Autenticação funciona** para todos os perfis
4. **Banco de dados populado** com dados de teste
5. **Scripts de manutenção funcionais**
6. **TODOs pedagógicos marcados** para os alunos
7. **Documentação completa**

### ⚠️ Sistema NÃO está pronto se:

- ❌ Algum teste falha
- ❌ Cadastro não funciona
- ❌ Login não funciona
- ❌ Erros no console ao iniciar
- ❌ Banco vazio
- ❌ Sem documentação

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique `logs/app.log`
2. Verifique console do navegador (F12)
3. Rode testes: `python -m pytest tests/ -v`
4. Consulte documentação em `docs/`

---

**Última atualização**: 20 de outubro de 2025
**Versão**: 1.0.0
**Projeto**: OBRATTO - Sistema de Gestão de Serviços e Produtos
