"""
SQL para tabela de pagamentos
"""

SQL_CRIAR_TABELA_PAGAMENTO = """
    CREATE TABLE IF NOT EXISTS pagamento (
        id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
        plano_id INTEGER NOT NULL,
        fornecedor_id INTEGER NOT NULL,
        mp_payment_id TEXT,
        mp_preference_id TEXT,
        valor REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        metodo_pagamento TEXT,
        data_criacao TEXT NOT NULL,
        data_aprovacao TEXT,
        external_reference TEXT,
        FOREIGN KEY (plano_id) REFERENCES plano (id_plano)
    )
"""

SQL_INSERIR_PAGAMENTO = """
    INSERT INTO pagamento (
        plano_id, fornecedor_id, mp_payment_id, mp_preference_id, 
        valor, status, metodo_pagamento, data_criacao, 
        data_aprovacao, external_reference
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_PAGAMENTO_POR_ID = """
    SELECT * FROM pagamento WHERE id_pagamento = ?
"""

SQL_OBTER_PAGAMENTO_POR_MP_ID = """
    SELECT * FROM pagamento WHERE mp_payment_id = ?
"""

SQL_OBTER_PAGAMENTO_POR_PREFERENCE = """
    SELECT * FROM pagamento WHERE mp_preference_id = ?
"""

SQL_ATUALIZAR_STATUS_PAGAMENTO = """
    UPDATE pagamento 
    SET status = ?, data_aprovacao = ?, metodo_pagamento = ?
    WHERE mp_payment_id = ?
"""

SQL_OBTER_PAGAMENTOS_FORNECEDOR = """
    SELECT p.*, pl.nome_plano 
    FROM pagamento p
    LEFT JOIN plano pl ON p.plano_id = pl.id_plano
    WHERE p.fornecedor_id = ?
    ORDER BY p.data_criacao DESC
"""

SQL_OBTER_PAGAMENTOS_PRESTADOR = """
    SELECT p.*, pl.nome_plano 
    FROM pagamento p
    LEFT JOIN plano pl ON p.plano_id = pl.id_plano
    WHERE p.prestador_id = ?
    ORDER BY p.data_criacao DESC
"""

SQL_OBTER_PAGAMENTOS_POR_STATUS = """
    SELECT p.*, pl.nome_plano 
    FROM pagamento p
    LEFT JOIN plano pl ON p.plano_id = pl.id_plano
    WHERE p.status = ?
    ORDER BY p.data_criacao DESC
"""

SQL_ATUALIZAR_PAGAMENTO = """
    UPDATE pagamento
    SET
        plano_id = ?,
        prestador_id = ?,
        mp_payment_id = ?,
        mp_preference_id = ?,
        valor = ?,
        status = ?,
        metodo_pagamento = ?,
        data_criacao = ?,
        data_aprovacao = ?,
        external_reference = ?
    WHERE id_pagamento = ?
"""