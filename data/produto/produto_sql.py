CRIAR_TABELA_PRODUTO = """
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    em_promocao INTEGER DEFAULT 0,
    desconto REAL DEFAULT 0.0,
    foto TEXT,
    fornecedor_id INTEGER
);
"""

INSERIR_PRODUTO = """
INSERT INTO produto (id, nome, descricao, preco, quantidade, em_promocao, desconto, foto, fornecedor_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

INSERIR_PRODUTO_SEM_ID = """
INSERT INTO produto (nome, descricao, preco, quantidade, em_promocao, desconto, foto, fornecedor_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_PRODUTO = """
SELECT id, nome, descricao, preco, quantidade, em_promocao, desconto, foto, fornecedor_id
FROM produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_ID = """
SELECT * FROM produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_PAGINA = """
SELECT * FROM produto
ORDER BY id
LIMIT ? OFFSET ?;
"""
OBTER_PRODUTO_POR_NOME = """
SELECT * FROM produto
WHERE nome LIKE ?;
"""

ATUALIZAR_PRODUTO = """
UPDATE produto
SET nome = ?,
    descricao = ?,
    preco = ?,
    quantidade = ?,
    em_promocao = ?,
    desconto = ?,
    foto = ?,
    fornecedor_id = ?
WHERE id = ?;
"""

OBTER_PRODUTOS_POR_FORNECEDOR = """
SELECT * FROM produto
WHERE fornecedor_id = ?
ORDER BY id
LIMIT ? OFFSET ?;
"""

DELETAR_PRODUTO = """
DELETE FROM produto
WHERE id = ?;
"""
