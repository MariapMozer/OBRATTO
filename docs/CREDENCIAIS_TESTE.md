# 🔑 Credenciais de Teste - Projeto OBRATTO

Este documento lista todas as credenciais de acesso para os usuários de teste criados pelo script `scripts/popular_banco.py`.

⚠️ **IMPORTANTE**: Estas credenciais são apenas para ambiente de **DESENVOLVIMENTO**. Nunca use em produção!

---

## 🔐 Senha Padrão

**TODOS os usuários de teste usam a mesma senha:**

```
Senha: Senha@123
```

---

## 👥 Usuários por Perfil

### 🛡️ Administradores (3)

| Nome | Email | Senha | Descrição |
|------|-------|-------|-----------|
| Admin Principal | `admin@obratto.com` | `Senha@123` | Administrador principal do sistema |
| Maria Administradora | `maria.admin@obratto.com` | `Senha@123` | Administradora de suporte |
| João Moderador | `joao.admin@obratto.com` | `Senha@123` | Moderador de conteúdo |

**Permissões**: Acesso total ao sistema, gerenciamento de usuários, planos e conteúdo.

---

### 👤 Clientes (5)

| Nome | Email | Senha | Gênero | Cidade |
|------|-------|-------|--------|--------|
| Maria Silva | `maria.silva@teste.com` | `Senha@123` | Feminino | Vitória |
| João Santos | `joao.santos@teste.com` | `Senha@123` | Masculino | Serra |
| Ana Paula Costa | `ana.costa@teste.com` | `Senha@123` | Feminino | Vila Velha |
| Carlos Eduardo Lima | `carlos.lima@teste.com` | `Senha@123` | Masculino | Cariacica |
| Fernanda Oliveira | `fernanda.oliveira@teste.com` | `Senha@123` | Feminino | Vitória |

**Permissões**: Solicitar orçamentos, avaliar prestadores, contratar serviços.

---

### 🔧 Prestadores de Serviço (5)

| Nome | Email | Senha | Área de Atuação | Razão Social |
|------|-------|-------|-----------------|--------------|
| Pedro Eletricista | `pedro.eletricista@teste.com` | `Senha@123` | Elétrica | Pedro Elétrica MEI |
| Carla Encanadora | `carla.encanadora@teste.com` | `Senha@123` | Hidráulica | Carla Hidráulica |
| Ricardo Pintor | `ricardo.pintor@teste.com` | `Senha@123` | Pintura | Ricardo Pinturas |
| Julia Jardineira | `julia.jardineira@teste.com` | `Senha@123` | Jardinagem | Julia Paisagismo |
| Marcos Pedreiro | `marcos.pedreiro@teste.com` | `Senha@123` | Construção Civil | Marcos Construções |

**Permissões**: Criar/editar serviços, responder orçamentos, gerenciar anúncios.

---

### 🏪 Fornecedores (5)

| Nome Fantasia | Email | Senha | Razão Social | CNPJ |
|---------------|-------|-------|--------------|------|
| Casa das Tintas | `contato@casadastintas.com` | `Senha@123` | Casa das Tintas Ltda | 11.111.111/0001-11 |
| Materiais Hidráulicos Silva | `vendas@materiaissilva.com` | `Senha@123` | Silva Materiais Hidráulicos Ltda | 22.222.222/0001-22 |
| Elétrica Total | `contato@eletricatotal.com` | `Senha@123` | Elétrica Total Comercial Ltda | 33.333.333/0001-33 |
| Jardinagem Verde Vida | `vendas@verdevida.com` | `Senha@123` | Verde Vida Jardinagem e Paisagismo Ltda | 44.444.444/0001-44 |
| Construção Forte | `comercial@construcaoforte.com` | `Senha@123` | Construção Forte Materiais de Construção Ltda | 55.555.555/0001-55 |

**Permissões**: Criar/editar produtos, gerenciar estoque, responder consultas.

---

## 📦 Produtos Cadastrados (15)

### Tintas - Casa das Tintas
- Tinta Acrílica Branca 18L - R$ 189,90
- Tinta Látex Amarela 3.6L - R$ 45,90
- Verniz Marítimo 900ml - R$ 67,50

### Hidráulica - Materiais Silva
- Registro de Pressão 1/2" - R$ 28,90
- Caixa D'água 1000L - R$ 320,00
- Tubo PVC 50mm 6m - R$ 42,50

### Elétrica - Elétrica Total
- Disjuntor Bipolar 40A - R$ 35,90
- Tomada 2P+T 10A Branca - R$ 8,50
- Fio Flexível 2.5mm 100m - R$ 120,00

### Jardinagem - Verde Vida
- Substrato Orgânico 15kg - R$ 22,90
- Grama Esmeralda m² - R$ 8,00
- Kit Ferramentas Jardinagem - R$ 89,90

### Construção - Construção Forte
- Cimento CP-II 50kg - R$ 32,50
- Areia Média m³ - R$ 85,00
- Tijolo Furado 8 Furos - R$ 0,65

---

## 💎 Planos de Assinatura (3)

| Plano | Valor Mensal | Limite de Serviços | Tipo |
|-------|--------------|-------------------|------|
| Básico | R$ 29,90 | 10 | Básico |
| Padrão | R$ 59,90 | 25 | Padrão |
| Premium | R$ 99,90 | Ilimitado | Premium |

---

## 🧪 Como Usar para Testes

### 1. Popular o Banco de Dados

```bash
# Limpar dados existentes (CUIDADO: remove todos os dados!)
python scripts/limpar_banco.py

# Popular com dados de teste
python scripts/popular_banco.py

# Gerar fotos placeholder
python scripts/gerar_fotos_teste.py
```

### 2. Iniciar o Servidor

```bash
uvicorn main:app --reload
```

### 3. Acessar o Sistema

```
http://localhost:8000
```

### 4. Testar Diferentes Perfis

1. **Teste como Cliente**:
   - Login: `maria.silva@teste.com`
   - Explore: buscar prestadores, solicitar orçamentos

2. **Teste como Prestador**:
   - Login: `pedro.eletricista@teste.com`
   - Explore: criar serviços, responder orçamentos

3. **Teste como Fornecedor**:
   - Login: `contato@casadastintas.com`
   - Explore: gerenciar produtos, responder consultas

4. **Teste como Admin**:
   - Login: `admin@obratto.com`
   - Explore: gerenciar usuários, moderar conteúdo

---

## 📸 Fotos de Teste

As fotos de teste são geradas automaticamente pelo script `gerar_fotos_teste.py`:

- **Usuários**: Avatares com iniciais do nome em cores variadas
- **Produtos**: Imagens coloridas com o nome do produto

Localização:
- `static/uploads/teste/usuarios/` - 18 fotos de perfil
- `static/uploads/teste/produtos/` - 15 fotos de produtos

---

## 🔒 Segurança

### ⚠️ AVISOS IMPORTANTES

1. **Nunca use estas credenciais em produção!**
2. **Nunca commit o arquivo `obratto.db` no Git!**
3. **A senha `Senha@123` é apenas para desenvolvimento!**
4. **Em produção, use senhas fortes e únicas para cada usuário!**

### Boas Práticas para Produção

```python
# ❌ NÃO FAÇA ISSO EM PRODUÇÃO:
SENHA_PADRAO = "Senha@123"

# ✅ FAÇA ISSO EM PRODUÇÃO:
import secrets
senha = secrets.token_urlsafe(16)  # Gera senha aleatória forte
```

---

## 📝 Notas Pedagógicas para Alunos

### Por que usar dados de teste?

1. **Desenvolvimento mais rápido**: Não precisa cadastrar dados manualmente toda vez
2. **Testes consistentes**: Todos os desenvolvedores usam os mesmos dados
3. **Demonstrações**: Facilita apresentar o sistema funcionando
4. **Aprendizado**: Permite explorar todas as funcionalidades

### O que NÃO fazer:

- ❌ Usar dados de teste em produção
- ❌ Usar senhas simples em produção
- ❌ Commitar banco de dados com dados sensíveis
- ❌ Expor credenciais em código versionado

### O que fazer:

- ✅ Usar variáveis de ambiente para credenciais
- ✅ Gerar senhas fortes em produção
- ✅ Implementar autenticação de 2 fatores
- ✅ Fazer backups regulares
- ✅ Implementar rate limiting

---

## 🆘 Problemas Comuns

### Não consigo fazer login

1. Verifique se o banco foi populado: `python scripts/popular_banco.py`
2. Confirme que está usando a senha correta: `Senha@123`
3. Verifique se o email está correto (sem espaços extras)

### Fotos não aparecem

1. Execute: `python scripts/gerar_fotos_teste.py`
2. Verifique se a pasta `static/uploads/teste/` existe
3. Confirme que o servidor tem permissão de leitura

### Banco de dados corrompido

```bash
# Limpar e recriar tudo:
python scripts/limpar_banco.py
python scripts/popular_banco.py
python scripts/gerar_fotos_teste.py
```

---

## 📚 Scripts Disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `popular_banco.py` | Popula o banco com dados de teste | `python scripts/popular_banco.py` |
| `limpar_banco.py` | Remove todos os dados (mantém tabelas) | `python scripts/limpar_banco.py` |
| `migrar_schema.py` | Adiciona colunas faltantes | `python scripts/migrar_schema.py` |
| `gerar_fotos_teste.py` | Gera fotos placeholder | `python scripts/gerar_fotos_teste.py` |

---

**Última atualização**: Fase 3 - Preparação do Banco de Dados

**Criado por**: Sistema de População Automática do OBRATTO
