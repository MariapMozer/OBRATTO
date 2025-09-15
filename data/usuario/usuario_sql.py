CRIAR_TABELA_USUARIO = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    cpf_cnpj TEXT NOT NULL,
    telefone TEXT NOT NULL,
    data_cadastro TEXT NOT NULL,
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    endereco TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL DEFAULT 'Cliente');

"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, email, senha, cpf_cnpj, telefone, data_cadastro, foto, token_redefinicao, data_token, endereco, tipo_usuario) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT ID, nome, email, senha, cpf_cnpj, telefone, data_cadastro, foto, token_redefinicao, data_token, endereco, tipo_usuario
FROM usuario
WHERE email = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT * FROM usuario WHERE id = ?;
"""

OBTER_USUARIO_POR_PAGINA = """
SELECT * FROM usuario
ORDER BY id
LIMIT ? OFFSET ?;
"""

#OBTER_USUARIO_POR_PERFIL = """
#OBTER_TODOS_POR_PERFIL
OBTER_USUARIOS_POR_PERFIL = """
SELECT * FROM usuario WHERE tipo_usuario = ?;
"""

ATUALIZAR_USUARIO = """
UPDATE usuario
SET nome = ?,
    email = ?,
    senha = ?,
    cpf_cnpj = ?,
    telefone = ?,
    data_cadastro = ?,
    foto = ?,
    token_redefinicao = ?,
    data_token = ?,
    endereco = ?,
    tipo_usuario = ?
WHERE id = ?
"""
ATUALIZAR_TIPO_USUARIO = """
UPDATE usuario
SET tipo_usuario = ?
WHERE id = ?
"""

ATUALIZAR_SENHA_USUARIO = """
UPDATE usuario
SET senha = ?
WHERE id = ?
"""

DELETAR_USUARIO = """
DELETE FROM usuario
WHERE id = ?
"""