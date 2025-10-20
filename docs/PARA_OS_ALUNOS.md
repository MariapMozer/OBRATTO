# 📚 Guia de Correções - Para os Alunos

**Professor**: Este documento lista todos os problemas identificados no código que precisam ser corrigidos pelos alunos.

**Alunos**: Cada problema está marcado com `TODO ALUNO:` no código. Use este guia como checklist.

---

## 🎯 Objetivo

Corrigir e melhorar o código implementado, aplicando as boas práticas aprendidas:
- ✅ Usar DTOs para validação
- ✅ Usar logger em vez de print
- ✅ Implementar funções vazias
- ✅ Remover/corrigir código comentado
- ✅ Usar flash messages para feedback

---

## 📋 Lista de Correções Necessárias

### 🔴 CRÍTICO - Funções Não Implementadas

#### 1. Edição de Perfil do Cliente (VAZIO)

**Arquivo**: `routes/cliente/cliente_perfil.py`
**Linha**: 64-98
**Problema**: Função `processar_edicao_perfil_cliente()` está vazia (apenas `pass`)

**O que fazer:**
1. Obter cliente do banco por ID
2. Validar se email já está em uso
3. Processar upload de foto (se enviada)
4. Atualizar dados no banco
5. Usar flash message
6. Redirecionar para perfil

**Exemplo de implementação:**
```python
try:
    # 1. Obter cliente atual
    cliente = cliente_repo.obter_cliente_por_id(usuario_logado["id"])
    if not cliente:
        informar_erro(request, "Cliente não encontrado")
        return RedirectResponse("/cliente/perfil", status.HTTP_303_SEE_OTHER)

    # 2. Verificar email duplicado
    if email != cliente.email:
        usuario_existente = usuario_repo.obter_usuario_por_email(email)
        if usuario_existente:
            informar_erro(request, "Email já está em uso")
            return RedirectResponse("/cliente/perfil/editar", status.HTTP_303_SEE_OTHER)

    # 3. Atualizar campos
    cliente.nome = nomeCompleto
    cliente.email = email
    cliente.telefone = telefone
    # ... atualizar outros campos

    # 4. Processar foto (se enviada)
    if foto and foto.filename:
        # Ver função alterar_foto() como exemplo
        pass

    # 5. Salvar no banco
    cliente_repo.atualizar_cliente(cliente)

    # 6. Flash message e redirect
    informar_sucesso(request, "Perfil atualizado com sucesso!")
    return RedirectResponse("/cliente/perfil", status.HTTP_303_SEE_OTHER)

except Exception as e:
    logger.error(f"Erro ao editar perfil: {e}")
    informar_erro(request, f"Erro ao atualizar perfil: {str(e)}")
    return RedirectResponse("/cliente/perfil/editar", status.HTTP_303_SEE_OTHER)
```

**Referências:**
- `routes/publico/publico_routes.py::processar_cadastro_cliente` (cadastro)
- `routes/cliente/cliente_perfil.py::alterar_foto` (upload de foto)

---

#### 2. Edição de Perfil do Prestador (INCOMPLETA)

**Arquivo**: `routes/prestador/prestador_perfil.py`
**Linha**: 74-118
**Problema**: Função recebe dados mas apenas retorna template sem processar

**O que está errado:**
- ❌ Recebe 11 parâmetros do formulário
- ❌ NÃO valida os dados
- ❌ NÃO atualiza o banco
- ❌ NÃO exibe mensagem de sucesso/erro
- ❌ Retorna template em vez de redirecionar

**O que fazer:**
1. Obter prestador do banco
2. Validar email duplicado
3. Atualizar campos
4. Salvar no banco
5. Flash message
6. Redirecionar

**Estrutura recomendada:**
```python
try:
    # 1. Obter prestador
    prestador = prestador_repo.obter_prestador_por_id(usuario_logado["id"])

    # 2. Validar email
    if email != prestador.email:
        if usuario_repo.obter_usuario_por_email(email):
            informar_erro(request, "Email já está em uso")
            return RedirectResponse("/prestador/perfil/editar", status.HTTP_303_SEE_OTHER)

    # 3. Atualizar campos
    prestador.nome = nome
    prestador.email = email
    prestador.telefone = telefone
    prestador.cpf_cnpj = cpf_cnpj
    prestador.estado = estado
    prestador.cidade = cidade
    prestador.rua = rua
    prestador.numero = numero
    prestador.bairro = bairro
    prestador.area_atuacao = area_atuacao
    prestador.razao_social = razao_social
    prestador.descricao_servicos = descricao_servicos

    # 4. Salvar
    prestador_repo.atualizar_prestador(prestador)

    # 5. Feedback
    informar_sucesso(request, "Perfil atualizado com sucesso!")
    logger.info(f"Prestador {prestador.id} atualizou perfil")

    # 6. Redirecionar
    return RedirectResponse("/prestador/perfil", status.HTTP_303_SEE_OTHER)

except Exception as e:
    logger.error(f"Erro ao atualizar prestador: {e}")
    informar_erro(request, f"Erro ao atualizar perfil: {str(e)}")
    return RedirectResponse("/prestador/perfil/editar", status.HTTP_303_SEE_OTHER)
```

**Referências:**
- `routes/publico/publico_routes.py::processar_cadastro_prestador`
- `routes/prestador/prestador_perfil.py::alterar_foto`

---

### 🟡 IMPORTANTE - Código Comentado

#### 3. Rota de Mensagens Comentada

**Arquivo**: `routes/publico/publico_routes.py`
**Linhas**: 825-881
**Problema**: 25 linhas de código comentadas sem explicação

**Análise:**
- Rota GET `/mensagens` para exibir caixa de mensagens
- **PROBLEMA DE SEGURANÇA**: Não usa `@requer_autenticacao()`
- Usa `obter_usuario_logado()` manualmente
- Função `organizar_conversas_por_contato()` não existe

**Decisões possíveis:**

**OPÇÃO A - REMOVER** (se não for necessária):
```python
# Simplesmente delete todo o bloco comentado (linhas 856-881)
```

**OPÇÃO B - IMPLEMENTAR** (se for necessária):
```python
@router.get("/mensagens")
@requer_autenticacao()  # ← ADICIONAR isto!
async def exibir_caixa_mensagens(
    request: Request,
    usuario_logado: Optional[dict] = None  # ← ADICIONAR isto!
):
    """Exibe a caixa de mensagens principal do usuário"""
    assert usuario_logado is not None

    # Obter mensagens do usuário
    mensagens = mensagem_repo.obter_mensagem_por_usuario(usuario_logado["id"])

    # IMPLEMENTAR: organizar mensagens por conversa
    conversas = {}  # TODO: implementar agrupamento

    return templates.TemplateResponse("publico/mensagens/mensagens.html", {
        "request": request,
        "usuario": usuario_logado,
        "conversas": conversas,
        "mensagens": mensagens
    })
```

**OPÇÃO C - MOVER** (se pertence a outro módulo):
- Mover para módulo específico (cliente, prestador, etc.)

**Ação recomendada**: Consulte o professor para decidir.

---

### 🟠 MÉDIO - Boas Práticas

#### 4. Uso de print() em vez de logger

**Arquivo**: `routes/fornecedor/fornecedor_produtos.py`
**Linhas**: 386, 388, 390
**Problema**: Usando `print()` em vez do sistema de logging

**Por que é ruim:**
- ❌ print() não grava em arquivo de log
- ❌ Não tem níveis (INFO, WARNING, ERROR)
- ❌ Não inclui timestamp automático
- ❌ Dificulta debugging em produção

**Como corrigir:**

**ANTES:**
```python
print(f"Imagem removida: {caminho_completo}")
print(f"Arquivo não encontrado: {caminho_completo}")
print(f"Erro ao remover imagem {caminho_completo}: {e}")
```

**DEPOIS:**
```python
logger.info(f"Imagem removida: {caminho_completo}")
logger.warning(f"Arquivo não encontrado: {caminho_completo}")
logger.error(f"Erro ao remover imagem {caminho_completo}: {e}")
```

**Verificar também em:**
- `routes/publico/publico_routes.py`
- `routes/administrador/administrador_servicos.py`
- `routes/prestador/prestador_servicos.py`

---

## 🧪 Como Testar Suas Correções

### 1. Testes Automatizados

```bash
# Rodar todos os testes
python -m pytest tests/ -v

# Devem continuar passando: 122/122
```

### 2. Testes Manuais

#### Testar Edição de Perfil do Cliente:
1. Popular banco: `python scripts/popular_banco.py`
2. Iniciar servidor: `uvicorn main:app --reload`
3. Login como cliente: `maria.silva@teste.com` / `Senha@123`
4. Acessar: http://localhost:8000/cliente/perfil/editar
5. Alterar dados e salvar
6. Verificar:
   - ✅ Dados foram salvos no banco
   - ✅ Flash message apareceu
   - ✅ Redirecionou para perfil
   - ✅ Log foi registrado

#### Testar Edição de Perfil do Prestador:
1. Login como prestador: `pedro.eletricista@teste.com` / `Senha@123`
2. Acessar: http://localhost:8000/prestador/perfil/editar
3. Alterar dados e salvar
4. Verificar mesmos itens acima

---

## 📚 Recursos de Referência

### Exemplos de Código Correto

**Cadastro com DTO (publico_routes.py):**
```python
@router.post("/cadastro/cliente")
async def processar_cadastro_cliente(request: Request):
    try:
        # 1. Obter dados do formulário
        form_data = await request.form()

        # 2. Validar com DTO
        dto = CriarClienteDTO(
            nome=form_data.get("nomeCompleto"),
            email=form_data.get("email"),
            # ...
        )

        # 3. Verificar duplicatas
        if usuario_repo.obter_usuario_por_email(dto.email):
            informar_erro(request, "Email já está em uso")
            return RedirectResponse("/cadastro/cliente", status.HTTP_303_SEE_OTHER)

        # 4. Criar objeto
        cliente = Cliente(
            id=0,
            nome=dto.nome,
            email=dto.email,
            # ...
        )

        # 5. Salvar
        cliente_id = cliente_repo.inserir_cliente(cliente)

        # 6. Feedback
        informar_sucesso(request, "Cadastro realizado!")
        logger.info(f"Cliente {cliente_id} cadastrado")

        # 7. Redirecionar
        return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        logger.warning(f"Dados inválidos: {e}")
        informar_erro(request, "Dados inválidos")
        return RedirectResponse("/cadastro/cliente", status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(f"Erro no cadastro: {e}")
        informar_erro(request, "Erro ao cadastrar")
        return RedirectResponse("/cadastro/cliente", status.HTTP_303_SEE_OTHER)
```

### Importações Necessárias

```python
import logging
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from typing import Optional
from util.auth_decorator import requer_autenticacao
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates

# Configurar logger
logger = logging.getLogger(__name__)
```

---

## ✅ Checklist de Correções

Marque conforme for completando:

- [ ] **1. Implementar edição de perfil do cliente**
  - [ ] Obter cliente do banco
  - [ ] Validar email duplicado
  - [ ] Processar foto (se enviada)
  - [ ] Atualizar no banco
  - [ ] Flash message
  - [ ] Logger
  - [ ] Testar manualmente
  - [ ] Testar com pytest

- [ ] **2. Implementar edição de perfil do prestador**
  - [ ] Obter prestador do banco
  - [ ] Validar email duplicado
  - [ ] Atualizar todos os campos
  - [ ] Salvar no banco
  - [ ] Flash message
  - [ ] Logger
  - [ ] Testar manualmente
  - [ ] Testar com pytest

- [ ] **3. Revisar código comentado de mensagens**
  - [ ] Decidir: remover, implementar ou mover
  - [ ] Se implementar: adicionar @requer_autenticacao()
  - [ ] Se implementar: adicionar usuario_logado
  - [ ] Se implementar: testar
  - [ ] Se remover: deletar bloco completo

- [ ] **4. Substituir print() por logger**
  - [ ] fornecedor_produtos.py (3 prints)
  - [ ] publico_routes.py (verificar)
  - [ ] administrador_servicos.py (verificar)
  - [ ] prestador_servicos.py (verificar)
  - [ ] Testar se logs aparecem em arquivo

- [ ] **5. Validação Final**
  - [ ] Todos os 122 testes passando
  - [ ] Servidor inicia sem erros
  - [ ] Todas as rotas públicas OK
  - [ ] Edição de perfis funcionando
  - [ ] Flash messages aparecendo
  - [ ] Logs sendo gravados

---

## 🆘 Problemas Comuns e Soluções

### "AttributeError: 'NoneType' object has no attribute 'id'"

**Causa**: Não verificou se objeto existe antes de acessar

**Solução:**
```python
cliente = cliente_repo.obter_cliente_por_id(id)
if not cliente:
    informar_erro(request, "Cliente não encontrado")
    return RedirectResponse("/erro", status.HTTP_303_SEE_OTHER)

# Agora pode usar cliente.id com segurança
```

### "Flash message não aparece"

**Causa**: Redirecionamento incorreto ou template sem suporte

**Solução:**
1. Usar `status.HTTP_303_SEE_OTHER` no redirect
2. Verificar se template tem código para exibir mensagens
3. Ver `templates/publico/home.html` como exemplo

### "Logger não grava em arquivo"

**Causa**: Logger não foi configurado

**Solução:**
```python
import logging

# No início do arquivo
logger = logging.getLogger(__name__)

# Usar
logger.info("mensagem")
logger.error("erro")
```

### "Teste falha após minha correção"

**Causa**: Alterou comportamento esperado

**Solução:**
1. Ler o teste para entender o que ele espera
2. Ajustar código ou teste conforme necessário
3. Consultar professor se não souber

---

## 📖 Documentação Adicional

- **Padrões do projeto**: Ver `docs/AUDITORIA_INICIAL.md`
- **Credenciais de teste**: Ver `docs/CREDENCIAIS_TESTE.md`
- **Scripts disponíveis**: Ver `docs/RESUMO_EXECUCAO.md`

---

## 💡 Dicas Finais

1. **Faça uma correção por vez** - Não tente corrigir tudo de uma vez
2. **Teste após cada correção** - Rode pytest e teste manualmente
3. **Use os exemplos** - O código de publico_routes.py é referência
4. **Consulte o professor** - Quando tiver dúvidas
5. **Commit frequentemente** - Faça commits pequenos e descritivos
6. **Leia os TODOs completos** - Tem dicas valiosas no código

---

**Bom trabalho! 🚀**

**Lembre-se**: O objetivo não é apenas fazer funcionar, mas fazer da forma CORRETA, aplicando as boas práticas aprendidas.
