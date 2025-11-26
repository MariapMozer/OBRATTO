import sqlite3
import pytest
from datetime import datetime
from data.notificacao.notificacao_model import Notificacao
from data.notificacao.notificacao_repo import (
    criar_tabela_notificacao,
    inserir_notificacao,
    obter_notificacao,
    obter_notificacao_por_id,
    atualizar_notificacao,
    deletar,
    obter_notificacao_por_pagina
)
from data.usuario.usuario_repo import criar_tabela_usuario

class TestNotificacaoRepo:

    def test_criar_tabela_notificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        # Act
        resultado = criar_tabela_notificacao()
        # Assert
        assert resultado is True, "A criação da tabela notificacao deveria retornar True"

    def inserir_notificacao_para_teste(self):
        #Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()
        #Act
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=1,
            mensagem="Nova notificação",
            data_hora=datetime.now(),
            tipo_notificacao="info",
            visualizar=False
        )
        #Assert
        return inserir_notificacao(notificacao)

    def test_inserir_notificacao(self, test_db):
        #Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()
        #Act
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=1,
            mensagem="Nova notificação",
            data_hora=datetime.now(),
            tipo_notificacao="info",
            visualizar=False
        )

        id_notificacao = inserir_notificacao(notificacao)
        print(f"ID inserido: {id_notificacao}")
        assert id_notificacao is not None

        notificacao_db = obter_notificacao_por_id(id_notificacao)
        print(f"Notificação obtida do DB: {notificacao_db}")
        #Assert
        assert notificacao_db is not None

    def test_obter_notificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()
        # Act
        id_notificacao = self.inserir_notificacao_para_teste()
        notificacoes = obter_notificacao()
        # Assert
        assert len(notificacoes) > 0

    def test_obter_notificacao_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()
        # Act
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=1,
            mensagem="Notificação específica",
            data_hora=datetime.now(),
            tipo_notificacao="alerta",
            visualizar=False
        )
        id_notificacao = inserir_notificacao(notificacao)
        print("ID inserido:", id_notificacao)
        assert id_notificacao is not None
        notificacao_db = obter_notificacao_por_id(id_notificacao)
        print("Notificação obtida:", notificacao_db)
        assert notificacao_db is not None, "A notificação obtida não deve ser None"
        assert notificacao_db.mensagem == "Notificação específica"

    def test_obter_fornecedor_por_pagina(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()

        for i in range(15):
            notificacao = Notificacao(
                id_notificacao=0,
                id_usuario=1,
                mensagem="Notificação específica",
                data_hora=datetime.now(),
                tipo_notificacao="alerta",
                visualizar=False
            )
            
            inserir_notificacao(notificacao)

        with sqlite3.connect(test_db) as conn:
            notificacao_pagina_1 = obter_notificacao_por_pagina(conn, limit=10, offset=0)
            notificacao_pagina_2 = obter_notificacao_por_pagina(conn, limit=10, offset=10)
            notificacao_pagina_3 = obter_notificacao_por_pagina(conn, limit=10, offset=20)
        # Assert
        assert len(notificacao_pagina_1) == 10, "A primeira página deveria conter 10 notificacoes"
        assert len(notificacao_pagina_2) == 5, "A segunda página deveria conter os 5 notificacoes restantes"
        assert len(notificacao_pagina_3) == 0, "A terceira página não deveria conter nenhuma notificacao"
        # Opcional
        ids_pagina_1 = {n.id_notificacao for n in notificacao_pagina_1}
        ids_pagina_2 = {n.id_notificacao for n in notificacao_pagina_2}
        assert ids_pagina_1.isdisjoint(ids_pagina_2), "As notificacoes da página 1 não devem se repetir na página 2"    

    def test_atualizar_notificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()
        # Act
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=1,
            mensagem="Notificação antiga",
            data_hora=datetime.now(),
            tipo_notificacao="info",
            visualizar=False
        )
        # Act
        id_notificacao = inserir_notificacao(notificacao)
        assert id_notificacao is not None
        notificacao_atualizada = obter_notificacao_por_id(id_notificacao)
        assert notificacao_atualizada is not None
        notificacao_atualizada.mensagem = "Notificação atualizada"
        resultado = atualizar_notificacao(notificacao_atualizada)
        # Assert
        assert resultado is True

    def test_deletar_notificacao(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_notificacao()
        # Act
        notificacao = Notificacao(
            id_notificacao=0,
            id_usuario=1,
            mensagem="Notificação para deletar",
            data_hora=datetime.now(),
            tipo_notificacao="info",
            visualizar=False
        )
        id_notificacao = inserir_notificacao(notificacao)
        assert id_notificacao is not None
        resultado = deletar(id_notificacao)
        # Assert
        assert resultado is True
