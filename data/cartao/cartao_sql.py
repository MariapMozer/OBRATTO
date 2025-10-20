"""
SQL statements para gerenciamento de cartões de crédito
"""

# Criar tabela de cartões
CRIAR_TABELA_CARTAO = """
CREATE TABLE IF NOT EXISTS cartao_credito (
    id_cartao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fornecedor INTEGER NOT NULL,
    nome_titular TEXT NOT NULL,
    numero_cartao_criptografado TEXT NOT NULL,
    ultimos_4_digitos TEXT NOT NULL,
    mes_vencimento TEXT NOT NULL,
    ano_vencimento TEXT NOT NULL,
    bandeira TEXT NOT NULL,
    apelido TEXT NOT NULL,
    principal BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TEXT NOT NULL,
    data_atualizacao TEXT NOT NULL,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor (id_fornecedor)
);
"""

# Inserir cartão
INSERIR_CARTAO = """
INSERT INTO cartao_credito (
    id_fornecedor, nome_titular, numero_cartao_criptografado, 
    ultimos_4_digitos, mes_vencimento, ano_vencimento, 
    bandeira, apelido, principal, ativo, data_criacao, data_atualizacao
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Obter cartões do fornecedor
OBTER_CARTOES_FORNECEDOR = """
SELECT id_cartao, id_fornecedor, nome_titular, numero_cartao_criptografado,
       ultimos_4_digitos, mes_vencimento, ano_vencimento, bandeira,
       apelido, principal, ativo, data_criacao, data_atualizacao
FROM cartao_credito 
WHERE id_fornecedor = ? AND ativo = TRUE
ORDER BY principal DESC, data_criacao DESC
"""

# Obter cartões por prestador
OBTER_CARTOES_POR_PRESTADOR = """
SELECT id_cartao, id_prestador, nome_titular, numero_cartao_criptografado,
       ultimos_4_digitos, mes_vencimento, ano_vencimento, bandeira,
       apelido, principal, ativo, data_criacao, data_atualizacao
FROM cartao_credito 
WHERE id_prestador = ? AND ativo = TRUE
ORDER BY principal DESC, data_criacao DESC
"""

# Obter cartão por ID
OBTER_CARTAO_POR_ID = """
SELECT id_cartao, id_fornecedor, nome_titular, numero_cartao_criptografado,
       ultimos_4_digitos, mes_vencimento, ano_vencimento, bandeira,
       apelido, principal, ativo, data_criacao, data_atualizacao
FROM cartao_credito 
WHERE id_cartao = ? AND ativo = TRUE
"""

# Obter cartão principal
OBTER_CARTAO_PRINCIPAL = """
SELECT id_cartao, id_fornecedor, nome_titular, numero_cartao_criptografado,
       ultimos_4_digitos, mes_vencimento, ano_vencimento, bandeira,
       apelido, principal, ativo, data_criacao, data_atualizacao
FROM cartao_credito 
WHERE id_fornecedor = ? AND principal = TRUE AND ativo = TRUE
"""

# Atualizar cartão
ATUALIZAR_CARTAO = """
UPDATE cartao_credito SET 
    nome_titular = ?, apelido = ?, principal = ?, data_atualizacao = ?
WHERE id_cartao = ?
"""

# Desativar cartão (soft delete)
DESATIVAR_CARTAO = """
UPDATE cartao_credito SET 
    ativo = FALSE, data_atualizacao = ?
WHERE id_cartao = ?
"""

# Remover status principal de outros cartões
REMOVER_PRINCIPAL_OUTROS = """
UPDATE cartao_credito SET 
    principal = FALSE, data_atualizacao = ?
WHERE id_fornecedor = ? AND id_cartao != ?
"""

# Definir cartão como principal
DEFINIR_PRINCIPAL = """
UPDATE cartao_credito SET 
    principal = TRUE, data_atualizacao = ?
WHERE id_cartao = ?
"""
