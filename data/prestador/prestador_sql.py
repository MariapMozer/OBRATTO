CRIAR_TABELA_PRESTADOR = """
CREATE TABLE IF NOT EXISTS prestador (
    id INTEGER PRIMARY KEY,
    area_atuacao TEXT NOT NULL,
    razao_social TEXT,
    descricao_servicos TEXT,
    selo_confianca INTEGER DEFAULT 0,
    FOREIGN KEY (id) REFERENCES usuario(id)
);
"""
INSERIR_PRESTADOR = """
INSERT INTO prestador (id, area_atuacao, razao_social, descricao_servicos, selo_confianca)
VALUES (?, ?, ?, ?, ?);
"""

OBTER_PRESTADOR = """
SELECT
    p.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.cep,
    u.complemento,
    u.estado,
    u.cidade,
    u.rua,
    u.numero,
    u.bairro,
    u.data_cadastro,
    p.area_atuacao,
    u.tipo_usuario,
    p.razao_social,
    p.descricao_servicos,
    p.selo_confianca,
    u.foto,
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
    u.cep,
    u.complemento,
    u.estado,
    u.cidade,
    u.rua,
    u.numero,
    u.bairro,
    u.data_cadastro,
    p.area_atuacao,
    p.razao_social,
    p.descricao_servicos,
    p.selo_confianca,
    u.tipo_usuario,
    u.foto,
    u.token_redefinicao,
    u.data_token
FROM prestador p
JOIN usuario u ON p.id = u.id
WHERE p.id = ?;
"""
OBTER_PRESTADOR_POR_PAGINA = """
SELECT u.id, u.nome, u.email, u.senha, u.cpf_cnpj, u.telefone, u.cep, u.complemento, u.estado, u.cidade,  u.rua, u.numero, u.bairro,
       u.data_cadastro, p.area_atuacao, p.razao_social, p.descricao_servicos, p.selo_confianca, u.tipo_usuario, u.foto,
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
    u.cep,
    u.complemento,
    u.estado,
    u.cidade,
    u.rua,
    u.numero,
    u.bairro,
    u.data_cadastro,
    p.area_atuacao,
    p.razao_social,
    p.descricao_servicos,
    p.selo_confianca,
    u.tipo_usuario,
    u.foto,
    u.token_redefinicao,
    u.data_token
FROM prestador p
JOIN usuario u ON p.id = u.id
WHERE u.email = ?;
"""

ATUALIZAR_PRESTADOR = """
UPDATE prestador
SET area_atuacao = ?, razao_social = ?, descricao_servicos = ?, selo_confianca = ?
WHERE id = ?;
"""
DELETAR_PRESTADOR = """
DELETE FROM prestador WHERE id = ?;
"""