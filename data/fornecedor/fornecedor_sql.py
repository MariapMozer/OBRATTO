
CRIAR_TABELA_FORNECEDOR = """
CREATE TABLE IF NOT EXISTS fornecedor (
    id INTEGER PRIMARY KEY, 
    razao_social TEXT NOT NULL,
    selo_confianca INTEGER DEFAULT 0,
    FOREIGN KEY (id) REFERENCES usuario(id) 
);
"""


INSERIR_FORNECEDOR = """
INSERT INTO fornecedor (id, razao_social, selo_confianca)
VALUES (?, ?, ?);
"""


OBTER_FORNECEDOR = """
SELECT
    f.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.endereco,
    f.razao_social,
    f.selo_confianca,
    u.tipo_usuario
FROM fornecedor f
JOIN usuario u ON f.id = u.id
ORDER BY u.nome;
"""


OBTER_FORNECEDOR_POR_ID = """
SELECT
    f.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.endereco,
    f.razao_social,
    f.selo_confianca,
    u.tipo_usuario
FROM fornecedor f
JOIN usuario u ON f.id = u.id
WHERE f.id = ?;
"""


OBTER_FORNECEDOR_POR_PAGINA = """
SELECT u.id, u.nome, u.email, u.senha, u.cpf_cnpj, u.telefone,
       u.data_cadastro, u.endereco, f.razao_social, f.selo_confianca, u.tipo_usuario
FROM usuario u
JOIN fornecedor f ON f.id = u.id
ORDER BY f.razao_social
LIMIT ? OFFSET ?;
"""


OBTER_FORNECEDOR_POR_EMAIL = """
SELECT
    f.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.endereco,
    f.razao_social,
    f.selo_confianca,
    u.tipo_usuario
FROM fornecedor f
JOIN usuario u ON f.id = u.id
WHERE u.email = ?;
"""



ATUALIZAR_FORNECEDOR = """
UPDATE fornecedor
SET razao_social = ?, selo_confianca = ?
WHERE id = ?;
"""

DELETAR_FORNECEDOR = """
DELETE FROM fornecedor
WHERE id = ?;
"""