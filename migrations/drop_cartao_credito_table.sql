-- Migration: Remover tabela cartao_credito
-- Data: 2025-10-20
-- Descrição: Remove tabela de armazenamento de cartões de crédito.
--            Cartões não são mais armazenados localmente por questões de segurança.
--            Pagamentos agora usam tokenização via Mercado Pago.

-- Remover tabela de cartões de crédito
DROP TABLE IF EXISTS cartao_credito;

-- Nota: A tabela 'pagamento' (histórico de transações) é mantida intacta.
-- Nota: Usuários com assinaturas recorrentes precisarão reautorizar pagamentos via Mercado Pago.
