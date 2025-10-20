CRIAR_TABELA_ADMINISTRADOR = """
CREATE TABLE IF NOT EXISTS administrador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);
"""


INSERIR_ADMINISTRADOR = """
INSERT INTO administrador (id_usuario)                
VALUES (?)                                                                   
"""

OBTER_TODOS_ADMINISTRADORES = """
SELECT
    u.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.cep,
    u.rua,
    u.numero,
    u.complemento,
    u.bairro,
    u.cidade,
    u.estado,
    u.tipo_usuario,
    u.foto,
    u.token_redefinicao,
    u.data_token
FROM administrador ad
JOIN usuario u ON ad.id_usuario = u.id
ORDER BY u.nome;
"""

OBTER_ADMINISTRADOR_POR_ID = """
SELECT
    u.id,
    u.nome,
    u.email,
    u.senha,
    u.cpf_cnpj,
    u.telefone,
    u.data_cadastro,
    u.cep,
    u.rua,
    u.numero,
    u.complemento,
    u.bairro,
    u.cidade,
    u.estado,
    u.tipo_usuario,
    u.foto,
    u.token_redefinicao,
    u.data_token
FROM administrador ad
JOIN usuario u ON ad.id_usuario = u.id
WHERE ad.id = ?;
"""

ATUALIZAR_ADMINISTRADOR = """
UPDATE administrador
SET id_usuario = ?
WHERE id = ?
"""

DELETAR_ADMINISTRADOR = """
DELETE FROM administrador
WHERE id = ?
"""
