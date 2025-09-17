CRIAR_TABELA_INSCRICAO_PLANO = """
CREATE TABLE IF NOT EXISTS inscricao_plano (
    id_inscricao_plano INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fornecedor INTEGER,
    id_prestador INTEGER,
    id_plano INTEGER NOT NULL,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id),
    FOREIGN KEY (id_prestador) REFERENCES prestador(id),
    FOREIGN KEY (id_plano) REFERENCES plano(id)
);
"""


INSERIR_INSCRICAO_PLANO = """
INSERT INTO inscricao_plano (id_fornecedor, id_prestador, id_plano)
VALUES (?, ?, ?);
"""


OBTER_INSCRICAO_PLANO = """
SELECT * FROM inscricao_plano
ORDER BY id_inscricao_plano;
"""


OBTER_INSCRICAO_PLANO_POR_ID = """
SELECT * FROM inscricao_plano 
WHERE id_inscricao_plano = ?;
"""

OBTER_INSCRICAO_PLANO_POR_PAGINA = """
SELECT * FROM inscricao_plano
ORDER BY id_inscricao_plano
LIMIT ? OFFSET ?;
"""

OBTER_ASSINATURA_ATIVA_POR_PRESTADOR = """
SELECT * FROM inscricao_plano
WHERE id_prestador = ?
ORDER BY id_inscricao_plano DESC LIMIT 1
"""


ATUALIZAR_INSCRICAO_PLANO = """
UPDATE inscricao_plano
SET id_fornecedor = ?,
    id_prestador = ?,
    id_plano = ?
WHERE id_inscricao_plano = ?;
"""

DELETAR_INSCRICAO_PLANO = """
DELETE FROM inscricao_plano 
WHERE id_inscricao_plano = ?;
"""
