# ✅ Checklist de Entrega - Projeto OBRATTO

**Professor**: Use este checklist para validar se o projeto está pronto para entrega.

**Data**: ___/___/_____
**Validado por**: _______________________

---

## 🎯 Critérios Obrigatórios

### ✅ 1. Testes Automatizados

- [ ] **Todos os 122 testes passam** (`python -m pytest tests/ -v`)
- [ ] Sem warnings críticos
- [ ] Tempo de execução < 5 segundos

**Como verificar:**
```bash
python -m pytest tests/ -v
# Deve mostrar: 122 passed
```

**Status**: _____ (OK / FALHOU)
**Observações**: _________________________________

---

### ✅ 2. Infraestrutura Base

#### 2.1 Autenticação e Autorização
- [ ] `util/auth_decorator.py` existe e funcional
- [ ] Decorator `@requer_autenticacao()` funciona
- [ ] Decorator aceita lista de perfis permitidos
- [ ] Rotas protegidas bloqueiam acesso não autorizado
- [ ] Redirecionamento para /login funciona

#### 2.2 Sistema de Logging
- [ ] `util/logger_config.py` existe
- [ ] Logger configurado com RotatingFileHandler
- [ ] Arquivo `logs/app.log` é criado
- [ ] Logs incluem timestamp, nível e mensagem
- [ ] Logger usado em pelo menos 3 rotas diferentes

#### 2.3 Exception Handlers
- [ ] `util/exception_handlers.py` existe
- [ ] Handler para 404 (Not Found)
- [ ] Handler para 500 (Internal Server Error)
- [ ] Handler para 401 (Unauthorized)
- [ ] Handler para 403 (Forbidden)
- [ ] Handler para 422 (Validation Error)
- [ ] Handlers registrados no `main.py`

#### 2.4 Flash Messages / Toasts
- [ ] `util/flash_messages.py` existe
- [ ] Funções: `informar_sucesso()`, `informar_erro()`, `informar_alerta()`
- [ ] Integrado com Bootstrap 5 toasts
- [ ] Mensagens aparecem e desaparecem
- [ ] Testado em pelo menos 2 rotas

#### 2.5 Security
- [ ] `util/security.py` existe
- [ ] Função `criar_hash_senha()` usa bcrypt
- [ ] Função `verificar_senha()` funcional
- [ ] Senhas NUNCA armazenadas em plain text
- [ ] Token de redefinição de senha implementado

**Status Infraestrutura**: _____ (OK / REVISAR)
**Observações**: _________________________________

---

### ✅ 3. Banco de Dados

#### 3.1 Schema e Modelos
- [ ] Todas as tabelas criadas (`util/seed.py`)
- [ ] Models existem para todas as entidades
- [ ] Herança implementada (Usuario → Cliente/Prestador/Fornecedor)
- [ ] Foreign keys configuradas corretamente
- [ ] Campos NOT NULL respeitados

#### 3.2 Repositórios (Repositories)
- [ ] Repositório para cada entidade
- [ ] Métodos CRUD completos (Create, Read, Update, Delete)
- [ ] Uso de context manager (`with open_connection()`)
- [ ] Commits e rollbacks corretos
- [ ] Testes de repositório passando (100%)

#### 3.3 Scripts de Manutenção
- [ ] `scripts/popular_banco.py` existe e funciona
- [ ] Popula 18 usuários (3 admins, 5 clientes, 5 prestadores, 5 fornecedores)
- [ ] Popula 15 produtos
- [ ] Popula 3 planos
- [ ] `scripts/limpar_banco.py` existe (com confirmação)
- [ ] `scripts/migrar_schema.py` existe
- [ ] `scripts/gerar_fotos_teste.py` gera 33 fotos

**Teste rápido:**
```bash
python scripts/limpar_banco.py <<< "SIM"
python scripts/popular_banco.py
# Deve criar: 18 usuários, 15 produtos, 3 planos
```

**Status Banco de Dados**: _____ (OK / REVISAR)
**Observações**: _________________________________

---

### ✅ 4. Rotas Públicas (100% Funcionais)

#### 4.1 Home
- [ ] GET / retorna 200 OK
- [ ] Layout Bootstrap carrega
- [ ] Links de navegação funcionam
- [ ] Sem erros no console

#### 4.2 Login
- [ ] GET /login retorna 200 OK
- [ ] Formulário de login visível
- [ ] POST /login com credenciais válidas funciona
- [ ] POST /login com credenciais inválidas mostra erro
- [ ] Flash message aparece
- [ ] Redirecionamento por perfil funciona

**Teste:**
- Login: `admin@obratto.com` / `Senha@123` → Dashboard admin
- Login: `maria.silva@teste.com` / `Senha@123` → Dashboard cliente

#### 4.3 Cadastros
- [ ] GET /escolha_cadastro retorna 200 OK
- [ ] GET /cadastro/cliente retorna 200 OK
- [ ] GET /cadastro/prestador retorna 200 OK
- [ ] GET /cadastro/fornecedor retorna 200 OK
- [ ] POST /cadastro/cliente funciona (com DTO)
- [ ] POST /cadastro/prestador funciona (com DTO)
- [ ] POST /cadastro/fornecedor funciona (com DTO)
- [ ] Validações de DTO funcionam
- [ ] Flash messages aparecem
- [ ] Redirecionamento para /login após cadastro

**Teste rápido:**
- Cadastrar novo cliente com dados válidos
- Verificar se pode fazer login

**Status Rotas Públicas**: _____ (OK / REVISAR)
**Observações**: _________________________________

---

### ✅ 5. Segurança e Controle de Acesso

#### 5.1 Autenticação
- [ ] Rotas privadas redirecionam para /login se não autenticado
- [ ] Sessão mantém usuário logado
- [ ] Logout encerra sessão corretamente

#### 5.2 Autorização
- [ ] Cliente NÃO acessa rotas de prestador
- [ ] Prestador NÃO acessa rotas de fornecedor
- [ ] Fornecedor NÃO acessa rotas de admin
- [ ] Admin acessa todas as rotas
- [ ] Retorna 403 Forbidden para acesso não autorizado

#### 5.3 Validação de Dados
- [ ] DTOs implementados (Pydantic)
- [ ] Validação de email
- [ ] Validação de senha forte
- [ ] Validação de CPF/CNPJ
- [ ] Validação de campos obrigatórios

**Teste de segurança:**
```bash
# 1. Sem login, tentar acessar rota privada
curl -I http://localhost:8000/cliente/perfil
# Deve: Redirecionar para /login

# 2. Login como cliente, tentar acessar rota de admin
# Deve: Retornar 403 Forbidden
```

**Status Segurança**: _____ (OK / REVISAR)
**Observações**: _________________________________

---

## 🎓 Critérios Pedagógicos (para alunos)

### ✅ 6. Marcações TODO

- [ ] **Cliente perfil edição** marcado com TODO ALUNO
  - Arquivo: `routes/cliente/cliente_perfil.py:64`
  - Função vazia identificada e explicada

- [ ] **Prestador perfil edição** marcado com TODO ALUNO
  - Arquivo: `routes/prestador/prestador_perfil.py:74`
  - Função incompleta identificada e explicada

- [ ] **Código comentado** marcado com TODO ALUNO
  - Arquivo: `routes/publico/publico_routes.py:825`
  - Explicação sobre o que fazer

- [ ] **Uso de print()** marcado com TODO ALUNO
  - Arquivo: `routes/fornecedor/fornecedor_produtos.py:365`
  - Explicação sobre substituir por logger

**Verificação:**
```bash
# Buscar TODOs no código
grep -r "TODO ALUNO" routes/
# Deve encontrar pelo menos 4 marcações
```

**Status Marcações TODO**: _____ (OK / FALTAM)
**Quantos TODOs encontrados**: _____
**Observações**: _________________________________

---

### ✅ 7. Documentação para Alunos

- [ ] `docs/PARA_OS_ALUNOS.md` existe
- [ ] Lista todos os problemas a corrigir
- [ ] Exemplos de código correto
- [ ] Explicações pedagógicas claras
- [ ] Checklist de correções

- [ ] `docs/CREDENCIAIS_TESTE.md` existe
- [ ] Lista todos os usuários de teste
- [ ] Senha padrão documentada
- [ ] Instruções de uso claras

- [ ] `docs/ROTEIRO_TESTE_ENTREGA.md` existe
- [ ] Roteiro completo de testes E2E
- [ ] Tempo estimado indicado
- [ ] Passo a passo detalhado

**Status Documentação**: _____ (OK / FALTAM)
**Observações**: _________________________________

---

## 📊 Critérios Complementares

### ✅ 8. Qualidade do Código

#### 8.1 Padrões Adotados
- [ ] Repository pattern usado consistentemente
- [ ] DTOs usados em rotas públicas (referência)
- [ ] Logger usado (pelo menos em rotas públicas)
- [ ] Flash messages usados (pelo menos em rotas públicas)
- [ ] Template utility usado para configurar Jinja2

#### 8.2 Organização
- [ ] Estrutura de pastas clara
- [ ] Arquivos nomeados consistentemente
- [ ] Imports organizados
- [ ] Código sem `print()` desnecessários (exceto TODOs)

#### 8.3 Comentários
- [ ] Funções importantes comentadas
- [ ] TODOs pedagógicos explicativos
- [ ] Sem código morto (comentado sem razão)

**Status Qualidade**: _____ (BOM / MÉDIO / REVISAR)
**Observações**: _________________________________

---

### ✅ 9. Fotos e Assets

- [ ] `static/uploads/teste/usuarios/` contém 18 fotos
- [ ] `static/uploads/teste/produtos/` contém 15 fotos
- [ ] Fotos são placeholders com iniciais/nomes
- [ ] Fotos geradas por script (não manualmente)

**Verificação:**
```bash
ls -l static/uploads/teste/usuarios/ | wc -l
# Deve: 18 (+1 linha de total = 19)

ls -l static/uploads/teste/produtos/ | wc -l
# Deve: 15 (+1 linha de total = 16)
```

**Status Assets**: _____ (OK / FALTAM)
**Observações**: _________________________________

---

### ✅ 10. Servidor e Deploy

#### 10.1 Inicialização
- [ ] `uvicorn main:app --reload` inicia sem erros
- [ ] Porta 8000 disponível
- [ ] Mensagem "Application startup complete" aparece
- [ ] Sem exceções ao iniciar

#### 10.2 Rotas Registradas
- [ ] Rotas públicas registradas
- [ ] Rotas de cliente registradas
- [ ] Rotas de prestador registradas
- [ ] Rotas de fornecedor registradas
- [ ] Rotas de admin registradas

#### 10.3 Arquivos Estáticos
- [ ] `/static` está montado
- [ ] CSS/JS do Bootstrap carregam
- [ ] Imagens carregam
- [ ] Sem erros 404 para assets

**Status Servidor**: _____ (OK / PROBLEMAS)
**Observações**: _________________________________

---

## 🏁 Resumo Final

### Resultado Geral

**Total de itens obrigatórios**: 10 seções
**Total de itens completados**: _____ / 10

**Pontuação**: _____ %

### Status por Categoria

| Categoria | Status | Observações |
|-----------|--------|-------------|
| 1. Testes | ☐ OK ☐ FALHOU | |
| 2. Infraestrutura | ☐ OK ☐ REVISAR | |
| 3. Banco de Dados | ☐ OK ☐ REVISAR | |
| 4. Rotas Públicas | ☐ OK ☐ REVISAR | |
| 5. Segurança | ☐ OK ☐ REVISAR | |
| 6. TODOs Pedagógicos | ☐ OK ☐ FALTAM | |
| 7. Documentação | ☐ OK ☐ FALTAM | |
| 8. Qualidade | ☐ BOM ☐ MÉDIO ☐ REVISAR | |
| 9. Assets | ☐ OK ☐ FALTAM | |
| 10. Servidor | ☐ OK ☐ PROBLEMAS | |

---

## ✅ Decisão Final

- [ ] **APROVADO PARA ENTREGA** - Todos os critérios obrigatórios OK
- [ ] **APROVADO COM RESSALVAS** - Pequenos ajustes necessários
- [ ] **REQUER CORREÇÕES** - Problemas críticos encontrados

### Ressalvas / Correções Necessárias:

___________________________________________________________________
___________________________________________________________________
___________________________________________________________________
___________________________________________________________________

### Prazo para correções (se aplicável):

___/___/_____ às _____:_____

---

## 📋 Checklist Rápido (30 segundos)

**Comandos para validação rápida:**

```bash
# 1. Testes (deve: 122 passed)
python -m pytest tests/ --tb=line | tail -1

# 2. Popular banco (deve: criar 18 usuários, 15 produtos, 3 planos)
python scripts/popular_banco.py | grep "Total de"

# 3. Fotos (deve: 18 e 15)
ls static/uploads/teste/usuarios/ | wc -l
ls static/uploads/teste/produtos/ | wc -l

# 4. Servidor (deve: iniciar sem erros)
uvicorn main:app &
sleep 3
curl -I http://localhost:8000/
pkill -f uvicorn

# 5. TODOs (deve: encontrar marcações)
grep -r "TODO ALUNO" routes/ | wc -l
```

**Resultado esperado:**
- Testes: 122 passed ✅
- População: 18 usuários, 15 produtos, 3 planos ✅
- Fotos: 19 e 16 (com linha de total) ✅
- Servidor: HTTP/1.1 200 OK ✅
- TODOs: Pelo menos 4 ✅

---

## 📞 Suporte e Problemas

**Se encontrar problemas:**

1. Verifique `logs/app.log`
2. Rode testes com `-v` para mais detalhes
3. Consulte `docs/ROTEIRO_TESTE_ENTREGA.md`
4. Verifique documentação em `docs/`

---

**Checklist preenchido por**: _______________________
**Data**: ___/___/_____
**Hora**: _____:_____

**Assinatura**: _______________________

---

**Última atualização**: 20 de outubro de 2025
**Versão do Checklist**: 1.0.0
**Projeto**: OBRATTO - Sistema de Gestão de Serviços e Produtos
