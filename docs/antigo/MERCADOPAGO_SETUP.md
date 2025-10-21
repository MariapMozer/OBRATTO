# Guia de Configuração do Mercado Pago

## Integração Completa de Pagamentos com Mercado Pago

Este projeto agora inclui integração completa com o Mercado Pago para processar assinaturas de planos. Siga este guia para configurar e usar o sistema de pagamentos.

## 📋 Pré-requisitos

1. **Conta no Mercado Pago Developers**
   - Acesse: https://www.mercadopago.com.br/developers/
   - Crie uma conta ou faça login

2. **Python com dependências**
   - FastAPI
   - Mercado Pago SDK (`pip install mercadopago`)

## 🔧 Configuração

### 1. Obter Credenciais do Mercado Pago

1. Acesse o [Painel de Credenciais](https://www.mercadopago.com.br/developers/panel/credentials)
2. Copie suas credenciais de **TESTE** (para desenvolvimento):
   - Access Token (ex: `TEST-8888888888888888-121212-abc...`)
   - Public Key (ex: `TEST-abcdefgh-1234-5678-9012-...`)

### 2. Configurar Variáveis de Ambiente

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edite o arquivo `.env` com suas credenciais reais:
   ```
   MERCADOPAGO_ACCESS_TOKEN_TEST=SUA_ACCESS_TOKEN_AQUI
   MERCADOPAGO_PUBLIC_KEY_TEST=SUA_PUBLIC_KEY_AQUI
   ```

### 3. Configurar URLs de Callback

No arquivo `.env`, ajuste as URLs para seu ambiente:

**Para desenvolvimento local:**
```
BASE_URL=http://localhost:8000
```

**Para produção:**
```
BASE_URL=https://seudominio.com
```

## 🚀 Como Usar

### 1. Fluxo de Assinatura de Plano

1. **Cliente acessa:** `/fornecedor/planos/listar`
2. **Seleciona um plano e clica em:** "Assinar Plano"
3. **Sistema redireciona para:** `/fornecedor/planos/assinar?plano_id=X`
4. **Processar pagamento:** Sistema cria preferência no Mercado Pago
5. **Redirecionamento:** Cliente é levado para o Mercado Pago
6. **Retorno:** Cliente volta para uma das páginas de resultado

### 2. Páginas de Resultado

- **Sucesso:** `/fornecedor/planos/pagamento_sucesso`
  - Pagamento aprovado ✅
  - Plano ativado
  - Confetes animados 🎉

- **Erro:** `/fornecedor/planos/pagamento_erro`
  - Pagamento rejeitado ❌
  - Sugestões de solução
  - Botão para tentar novamente

- **Pendente:** `/fornecedor/planos/pagamento_pendente`
  - Pagamento em processamento ⏳
  - Auto-refresh da página
  - Verificação automática de status

### 3. Sistema de Webhooks

O sistema recebe notificações automáticas do Mercado Pago em:
- **Endpoint:** `/fornecedor/planos/webhook`
- **Função:** Atualiza status dos pagamentos automaticamente
- **Segurança:** Validação de origem (opcional)

## 🛠️ Estrutura dos Arquivos

```
routes/fornecedor/
├── fornecedor_planos.py          # Rotas principais de planos e pagamentos

templates/fornecedor/
├── listar_planos.html            # Lista planos disponíveis
├── assinar_plano.html            # Formulário de assinatura
├── processar_pagamento.html      # Redirecionamento para MP
├── pagamento_sucesso.html        # Página de sucesso
├── pagamento_erro.html           # Página de erro
└── pagamento_pendente.html       # Página de pendente

data/pagamento/
├── pagamento_model.py            # Modelo de dados
├── pagamento_repo.py             # Repository para banco
└── pagamento_sql.py              # SQL queries

utils/
└── mercadopago_config.py         # Configuração do MP
```

## 📊 Banco de Dados

### Tabela `pagamento`
```sql
CREATE TABLE pagamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id TEXT UNIQUE NOT NULL,
    plano_id INTEGER,
    valor REAL,
    status TEXT,
    metodo_pagamento TEXT,
    data_criacao DATETIME,
    data_atualizacao DATETIME
);
```

## 🔍 Teste da Integração

### 1. Testar Localmente

1. **Inicie o servidor:**
   ```bash
   python main.py
   ```

2. **Acesse:** http://localhost:8000/fornecedor/planos/listar

3. **Teste o fluxo completo:**
   - Listar planos → Assinar → Processar → Resultado

### 2. Dados de Teste do Mercado Pago

**Cartões para teste:**
- **Aprovado:** 4509 9535 6623 3704
- **Rejeitado:** 4013 5406 8274 6260
- **Pendente:** 4389 3540 6624 0647

**Dados adicionais:**
- **CVV:** 123
- **Validade:** 11/25
- **Nome:** APRO (aprovado) / OTHE (rejeitado)

## 🛡️ Segurança

### Ambiente de Produção

1. **Use credenciais de PRODUÇÃO:**
   ```
   MERCADOPAGO_ENVIRONMENT=production
   MERCADOPAGO_ACCESS_TOKEN_PROD=PROD-...
   MERCADOPAGO_PUBLIC_KEY_PROD=PROD-...
   ```

2. **Configure HTTPS obrigatório**

3. **Implemente validação de webhook**

4. **Use variáveis de ambiente seguras**

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro 401 - Unauthorized**
   - Verifique se as credenciais estão corretas
   - Confirme se está usando o ambiente certo (TEST/PROD)

2. **Webhook não funciona**
   - Verifique se a URL está acessível publicamente
   - Use ngrok para testes locais: `ngrok http 8000`

3. **Pagamento não atualiza status**
   - Verifique logs do webhook
   - Confirme se o banco de dados está acessível

### Debug

1. **Rota de debug:** `/fornecedor/planos/debug`
   - Mostra informações do banco
   - Lista planos disponíveis
   - Verifica configuração

2. **Logs do sistema:**
   - Verifique console para erros
   - Monitore chamadas de webhook

## 📞 Suporte

- **Documentação MP:** https://www.mercadopago.com.br/developers/pt/docs
- **SDK Python:** https://github.com/mercadopago/sdk-python
- **Simulador:** https://www.mercadopago.com.br/developers/pt/docs/checkout-pro/additional-content/test-integration

## ✅ Checklist de Implementação

- [x] ✅ SDK do Mercado Pago instalado
- [x] ✅ Configuração de credenciais (.env)
- [x] ✅ Modelo de dados de pagamento
- [x] ✅ Repository para pagamentos
- [x] ✅ Rotas de assinatura de planos
- [x] ✅ Templates de resultado (sucesso/erro/pendente)
- [x] ✅ Sistema de webhooks
- [x] ✅ Verificação de status automática
- [ ] ⏳ Configurar credenciais reais
- [ ] ⏳ Testar em ambiente de produção
- [ ] ⏳ Configurar domínio para webhooks

**Agora você tem uma integração completa de pagamentos com Mercado Pago!** 🎉
