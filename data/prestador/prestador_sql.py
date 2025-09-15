CRIAR_TABELA_PRESTADOR = """
CREATE TABLE IF NOT EXISTS prestador (
    id INTEGER PRIMARY KEY,
    area_atuacao TEXT NOT NULL,
    razao_social TEXT,
    descricao_servicos TEXT,
    FOREIGN KEY (id) REFERENCES usuario(id)
);
"""
INSERIR_PRESTADOR = """
INSERT INTO prestador (id, area_atuacao, razao_social, descricao_servicos)
VALUES (?, ?, ?, ?);
"""

OBTER_PRESTADOR = """
SELECT
    p.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.endereco,
    p.area_atuacao,
    u.tipo_usuario,
    p.razao_social,
    p.descricao_servicos,
    u.foto,
    u.data_cadastro,
    u.token_redefinicao,
    u.data_token
FROM prestador p
JOIN usuario u ON p.id = u.id
ORDER BY u.nome;
"""
OBTER_PRESTADOR_POR_ID = """
SELECT
    p.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.endereco,
    p.area_atuacao,
    p.razao_social,
    p.descricao_servicos,
    u.tipo_usuario,
    u.foto,
    u.data_cadastro,
    u.token_redefinicao,
    u.data_token
FROM prestador p
JOIN usuario u ON p.id = u.id
WHERE p.id = ?;
"""
OBTER_PRESTADOR_POR_PAGINA = """
SELECT u.id, u.nome, u.email, u.senha, u.cpf_cnpj, u.telefone,
       u.data_cadastro, u.endereco, p.area_atuacao, p.razao_social, p.descricao_servicos, u.tipo_usuario, u.foto,
    u.data_cadastro,
    u.token_redefinicao,
    u.data_token
FROM usuario u
JOIN prestador p ON p.id = u.id
ORDER BY p.area_atuacao
LIMIT ? OFFSET ?;
"""

OBTER_PRESTADOR_POR_EMAIL = """
SELECT
    p.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.endereco,
    p.area_atuacao,
    p.razao_social,
    p.descricao_servicos,
    u.tipo_usuario,
    u.data_cadastro,
    u.foto,
    u.token_redefinicao,
    u.data_token
FROM prestador p
JOIN usuario u ON p.id = u.id
WHERE u.email = ?;
"""

ATUALIZAR_PRESTADOR = """
UPDATE prestador
SET area_atuacao = ? razao_social = ?, descricao_servicos = ?,
WHERE id = ?;
"""
DELETAR_PRESTADOR = """
DELETE FROM prestador WHERE id = ?;
"""