CRIAR_TABELA_USUARIO = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    cpf_cnpj TEXT NOT NULL,
    telefone TEXT NOT NULL,
    cep TEXT NOT NULL,
    logradouro TEXT NOT NULL,
    numero TEXT NOT NULL,
    complemento TEXT NOT NULL,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    data_cadastro TEXT NOT NULL,
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    tipo_usuario TEXT NOT NULL DEFAULT 'Cliente');

"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, email, senha, cpf_cnpj, telefone, cep, logradouro, numero, complemento, bairro, cidade, estado, data_cadastro, foto, token_redefinicao, data_token, tipo_usuario) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT ID, nome, email, senha, cpf_cnpj, telefone,  cep, logradouro, numero, complemento, bairro, cidade, estado, data_cadastro, foto, token_redefinicao, data_token, tipo_usuario
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
    cep = ?,
    logradouro = ?,
    numero = ?,
    complemento = ?,
    bairro = ?,
    cidade = ?,
    estado = ?,
    data_cadastro = ?,
    foto = ?,
    token_redefinicao = ?,
    data_token = ?,
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


# Adicionar coluna foto à tabela existente (se não existir)
ADICIONAR_COLUNA_FOTO = """
ALTER TABLE usuario ADD COLUMN foto TEXT
"""

# Atualizar apenas a foto do usuário
ATUALIZAR_FOTO = """
UPDATE usuario SET foto = ? WHERE id = ?
"""

DELETAR_USUARIO = """
DELETE FROM usuario
WHERE id = ?
"""

ADICIONAR_COLUNA_FOTO = """
ALTER TABLE usuario ADD COLUMN foto TEXT;
"""
ATUALIZAR_FOTO = """
UPDATE usuario
SET foto = ?
WHERE id = ?
"""