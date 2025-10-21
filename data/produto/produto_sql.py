CRIAR_TABELA_produto = """
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

INSERIR_produto = """
INSERT INTO produto (id, nome, descricao, preco, quantidade, em_promocao, desconto, foto, fornecedor_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

INSERIR_produto_SEM_ID = """
INSERT INTO produto (nome, descricao, preco, quantidade, em_promocao, desconto, foto, fornecedor_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_produto = """
SELECT id, nome, descricao, preco, quantidade, em_promocao, desconto, foto, fornecedor_id
FROM produto
WHERE id = ?;
"""

OBTER_produto_POR_ID = """
SELECT * FROM produto 
WHERE id = ?;
"""

OBTER_produto_POR_PAGINA = """
SELECT * FROM produto
ORDER BY id
LIMIT ? OFFSET ?;
"""
OBTER_produto_POR_NOME = """
SELECT * FROM produto
WHERE nome LIKE ?;
"""

ATUALIZAR_produto = """
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

OBTER_produtoS_POR_FORNECEDOR = """
SELECT * FROM produto
WHERE fornecedor_id = ?
ORDER BY id
LIMIT ? OFFSET ?;
"""

DELETAR_produto = """
DELETE FROM produto
WHERE id = ?;
"""
