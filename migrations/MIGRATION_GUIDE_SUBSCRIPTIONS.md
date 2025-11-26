# Guia de Migração - Assinaturas Recorrentes

## Data: 2025-10-20
## Autor: Claude Code

## Contexto

O sistema OBRATTO removeu a funcionalidade de armazenamento local de cartões de crédito por questões de segurança e conformidade PCI DSS. Cartões de crédito não são mais armazenados no banco de dados local.

## Nova Arquitetura

- **Antes:** Cartões armazenados localmente (tabela `cartao_credito`)
- **Agora:** Tokenização via Mercado Pago (cartões gerenciados pelo gateway)

## Impacto em Assinaturas Ativas

Usuários com assinaturas recorrentes precisarão:
1. Reautorizar pagamentos via Mercado Pago
2. Fornecer dados do cartão novamente (não armazenados localmente)
3. Aceitar que o Mercado Pago gerenciará tokens para cobranças recorrentes

## Passos para Migração

### 1. Identificar Assinaturas Ativas

```sql
SELECT
    i.id_inscricao_plano,
    i.id_fornecedor,
    i.id_prestador,
    i.id_plano,
    p.nome_plano,
    p.valor_mensal
FROM inscricao_plano i
JOIN plano p ON i.id_plano = p.id_plano
WHERE i.data_cancelamento IS NULL;
```

### 2. Notificar Usuários

Enviar email/notificação para cada usuário com assinatura ativa:

```
Assunto: Atualização Importante - Reautorização de Pagamento Necessária

Olá [NOME],

Atualizamos nosso sistema de pagamentos para maior segurança.

Por questões de conformidade PCI DSS, não armazenamos mais dados de
cartões de crédito em nossos servidores. Agora usamos tokenização
segura via Mercado Pago.

AÇÃO NECESSÁRIA:
- Acesse sua conta em [URL]
- Reautorize seu pagamento recorrente
- Seus dados de cartão serão gerenciados de forma segura pelo Mercado Pago

Sua assinatura permanecerá ativa até: [DATA + 30 DIAS]

Att,
Equipe OBRATTO
```

### 3. Implementar Fluxo de Reautorização

No código, adicionar lógica para:

```python
# Pseudocódigo
if user.has_active_subscription() and not user.has_mp_token():
    # Redirecionar para página de reautorização
    redirect_to_reauthorization_page()
```

### 4. Criar Tokens no Mercado Pago

Para cada usuário que reautorizar:

```python
# 1. Criar customer no Mercado Pago
customer = mercadopago_service.create_customer(
    email=user.email,
    first_name=user.first_name,
    last_name=user.last_name,
    identification_type="CPF",
    identification_number=user.cpf
)

# 2. Obter token do cartão (gerado no frontend via MercadoPago.js)
card_token = request.form.get('card_token')

# 3. Salvar cartão no Mercado Pago (não localmente)
saved_card = mercadopago_service.save_card_to_customer(
    customer_id=customer['customer_id'],
    card_token=card_token
)

# 4. Criar assinatura recorrente
subscription = mercadopago_service.create_subscription(
    customer_id=customer['customer_id'],
    card_id=saved_card['card_id'],
    plan_value=plan.valor_mensal,
    plan_name=plan.nome_plano,
    external_reference=f"subscription_{plan.id_plano}_user_{user.id}"
)

# 5. Armazenar IDs do MP no banco (não os dados do cartão)
update_subscription(
    user_id=user.id,
    mp_customer_id=customer['customer_id'],
    mp_card_id=saved_card['card_id'],
    mp_subscription_id=subscription['subscription_id']
)
```

### 5. Adicionar Campos ao Banco

Atualizar tabela `inscricao_plano` para armazenar referências do MP:

```sql
ALTER TABLE inscricao_plano ADD COLUMN mp_customer_id TEXT;
ALTER TABLE inscricao_plano ADD COLUMN mp_card_id TEXT;
ALTER TABLE inscricao_plano ADD COLUMN mp_subscription_id TEXT;
```

### 6. Monitoramento

- Rastrear quantos usuários reautorizaram
- Enviar lembretes para usuários que não reautorizaram
- Após período de graça (30 dias), cancelar assinaturas não reautorizadas

## Timeline Sugerido

- **Dia 0:** Enviar primeira notificação
- **Dia 7:** Enviar lembrete
- **Dia 14:** Enviar segundo lembrete
- **Dia 21:** Enviar aviso final
- **Dia 30:** Cancelar assinaturas não reautorizadas

## Suporte

Preparar FAQ e suporte para dúvidas sobre:
- Por que precisam reautorizar
- Segurança da nova solução
- Como funciona a tokenização
- O que acontece com dados antigos (foram removidos)

## Rollback

Não há rollback disponível. Dados de cartões foram permanentemente removidos
do banco de dados (backup existe, mas não deve ser restaurado por questões de segurança).

## Conformidade

Esta migração melhora significativamente a conformidade com:
- PCI DSS (Payment Card Industry Data Security Standard)
- LGPD (Lei Geral de Proteção de Dados)
- Melhores práticas de segurança em pagamentos online
