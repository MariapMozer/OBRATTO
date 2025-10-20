import sys
import os

from data.anuncio.anuncio_repo import *
from data.fornecedor.fornecedor_repo import *
from data.usuario.usuario_repo import *

class TestAnuncioRepo:

    def test_criar_tabela_anuncio(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        resultado = criar_tabela_anuncio()
        assert resultado is True, "A tabela de anúncios não foi criada com sucesso."

    def test_inserir_anuncio(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Teste",
            email="dsiufu",
            senha="123456",
            cpf_cnpj="12345678901",
            telefone="1234567890",
            data_cadastro="2023-10-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        fornecedor = Fornecedor(
            id=0,
            nome="chico",
            email="chico@gmail.com",
            senha="1234567",
            cpf_cnpj="123456789",
            telefone="987654321",
            data_cadastro="2025-09-02",
            tipo_usuario="fornecedor",
            razao_social="fornecedor_LTDA",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)
        assert id_fornecedor is not None
        anuncio = Anuncio(
            id_anuncio=0,
            nome_anuncio="Anúncio Teste",
            id_fornecedor=id_fornecedor,
            data_criacao="2023-10-01",
            descricao="Descrição do anúncio",
            preco=100.0
        )

        id_anuncio = inserir_anuncio(anuncio)
        anuncio_db = obter_anuncio_por_nome("Anúncio Teste")

        assert id_anuncio is not None, "O anúncio não foi inserido com sucesso."
        assert anuncio_db is not None, "O anúncio não foi encontrado no banco de dados."
        assert anuncio_db.nome_anuncio == "Anúncio Teste", "O nome do anúncio não corresponde ao esperado."
        assert anuncio_db.preco == 100.0, "O preço do anúncio não corresponde ao esperado."
        assert anuncio_db.descricao == "Descrição do anúncio", "A descrição do anúncio não corresponde ao esperado."
        assert anuncio_db.id_fornecedor == id_fornecedor, "O fornecedor do anúncio não corresponde ao esperado."
        assert anuncio_db.data_criacao == "2023-10-01", "A data de criação do anúncio não corresponde ao esperado."

    def test_obter_todos_anuncios(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Teste",
            email="dsiufu",
            senha="123456",
            cpf_cnpj="12345678901",
            telefone="1234567890",
            data_cadastro="2023-10-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@example.com",
            senha="senha",
            cpf_cnpj="12345678901",
            telefone="1234567890",
            data_cadastro="2023-10-01",
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)
        assert id_fornecedor is not None

        anuncio = Anuncio(
            id_anuncio=0,
            nome_anuncio="Anúncio Teste",
            id_fornecedor=id_fornecedor,
            data_criacao="2023-10-01",
            descricao="Descrição do anúncio",
            preco=100.0
        )

        id_anuncio = inserir_anuncio(anuncio)
        anuncios = obter_todos_anuncios()
        anuncio_db = next((a for a in anuncios if a.nome_anuncio == "Anúncio Teste"), None)

        assert id_anuncio is not None, "O anúncio não foi inserido com sucesso."
        assert anuncio_db is not None, "O anúncio não foi encontrado no banco de dados."
        assert anuncio_db.nome_anuncio == "Anúncio Teste", "O nome do anúncio não corresponde ao esperado."
        assert anuncio_db.preco == 100.0, "O preço do anúncio não corresponde ao esperado."
        assert anuncio_db.descricao == "Descrição do anúncio", "A descrição do anúncio não corresponde ao esperado."
        assert anuncio_db.id_fornecedor == id_fornecedor, "O fornecedor do anúncio não corresponde ao esperado."
        assert anuncio_db.data_criacao == "2023-10-01", "A data de criação do anúncio não corresponde ao esperado."

    def test_obter_anuncio_por_nome(self, test_db):
    # Arrange
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Teste",
            email="teste@example.com",
            senha="123456",
            cpf_cnpj="12345678901",
            telefone="1234567890",
            data_cadastro="2023-10-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@example.com",
            senha="123456",
            cpf_cnpj="98765432100",
            telefone="0987654321",
            data_cadastro="2023-10-01",
            razao_social="Fornecedor LTDA",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)

        assert id_fornecedor is not None
        anuncio = Anuncio(
            id_anuncio=0,
            nome_anuncio="Anúncio Teste",
            id_fornecedor=id_fornecedor,
            data_criacao="2023-10-01",
            descricao="Descrição do anúncio",
            preco=100.0
        )

        # Act
        id_anuncio = inserir_anuncio(anuncio)
        anuncio_db = obter_anuncio_por_nome("Anúncio Teste")

        # Assert
        assert id_anuncio is not None, "O anúncio não foi inserido com sucesso."
        assert anuncio_db is not None, "O anúncio não foi encontrado no banco de dados."
        assert anuncio_db.nome_anuncio == "Anúncio Teste", "O nome do anúncio não corresponde ao esperado."
        assert anuncio_db.preco == 100.0, "O preço do anúncio não corresponde ao esperado."
        assert anuncio_db.descricao == "Descrição do anúncio", "A descrição do anúncio não corresponde ao esperado."
        assert anuncio_db.id_fornecedor == id_fornecedor, "O fornecedor do anúncio não corresponde ao esperado."
        assert anuncio_db.data_criacao == "2023-10-01", "A data de criação do anúncio não corresponde ao esperado."

    def test_obter_anuncio_por_id(self, test_db):
    # Arrange 
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(0, nome="Teste", email="dsiufu", senha="123456", cpf_cnpj="12345678901", telefone="1234567890", data_cadastro="2023-10-01", tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")
        id_usuario = inserir_usuario(usuario)
        fornecedor = Fornecedor(id=0, nome="Fornecedor", email="fornecedor@example.com", senha="senha", cpf_cnpj="12345678901", telefone="1234567890", data_cadastro="2023-10-01", razao_social="Fornecedor LTDA", tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")

        id_fornecedor = inserir_fornecedor(fornecedor)
        assert id_fornecedor is not None
        anuncio = Anuncio(0, nome_anuncio="Anúncio Teste", id_fornecedor=id_fornecedor, data_criacao="2023-10-01", descricao="Descrição do anúncio", preco=100.0)
        # Act
        id_anuncio = inserir_anuncio(anuncio)
        assert id_anuncio is not None
        anuncio_db = obter_anuncio_por_id(id_anuncio)
        # Asserts 
        assert id_anuncio is not None, "O anúncio não foi inserido com sucesso."
        assert anuncio_db is not None, "O anúncio não foi encontrado no banco de dados."
        assert anuncio_db.nome_anuncio == "Anúncio Teste", "O nome do anúncio não corresponde ao esperado."
        assert anuncio_db.preco == 100.0, "O preço do anúncio não corresponde ao esperado."
        assert anuncio_db.descricao == "Descrição do anúncio", "A descrição do anúncio não corresponde ao esperado."
        assert anuncio_db.id_fornecedor == id_fornecedor, "O fornecedor do anúncio não corresponde ao esperado."
        assert anuncio_db.data_criacao == "2023-10-01", "A data de criação do anúncio não corresponde ao esperado."

    def test_obter_anuncio_paginado(self, test_db):
    # Arrange 
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Fornecedor Paginado",
            email="fornecedor@exemplo.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="999999999",
            data_cadastro="2023-01-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        assert id_usuario is not None
        fornecedor = Fornecedor(
            id=id_usuario,
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            cpf_cnpj=usuario.cpf_cnpj,
            telefone=usuario.telefone,
            data_cadastro=usuario.data_cadastro,
            cep=usuario.cep,
            rua=usuario.rua,
            numero=usuario.numero,
            complemento=usuario.complemento,
            bairro=usuario.bairro,
            cidade=usuario.cidade,
            estado=usuario.estado,
            razao_social="Fornecedor LTDA",
            tipo_usuario=usuario.tipo_usuario
        )
        id_fornecedor = inserir_fornecedor(fornecedor)

        assert id_fornecedor is not None
        for i in range(5):
            anuncio = Anuncio(
                id_anuncio=0,
                nome_anuncio=f"Anúncio {i}",
                id_fornecedor=id_fornecedor,
                data_criacao="2023-01-01",
                descricao=f"Descrição {i}",
                preco=10.0 * i
            )
            inserir_anuncio(anuncio)

        # Act – executar a função a ser testada
        limit = 3
        offset = 0
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    a.id_anuncio,
                    a.nome_anuncio,
                    a.id_fornecedor,
                    a.data_criacao,
                    a.descricao,
                    a.preco,
                    u.nome AS nome_fornecedor
                FROM anuncio a
                JOIN fornecedor f ON a.id_fornecedor = f.id
                JOIN usuario u ON f.id = u.id
                ORDER BY a.id_anuncio
                LIMIT ? OFFSET ?
            """, (limit, offset))
            rows = cursor.fetchall()

        # Assert – verificar se o retorno está correto
        assert len(rows) == limit, f"Esperado {limit} anúncios, mas retornaram {len(rows)}"
        for i, row in enumerate(rows):
            assert row["nome_anuncio"] == f"Anúncio {i}", f"Nome do anúncio incorreto no índice {i}"
            assert row["nome_fornecedor"] == "Fornecedor Paginado", "Nome do fornecedor incorreto"

    def test_obter_anuncio_por_termo_paginado(self, test_db):
    # Arrange – preparar tabelas e dados
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Fornecedor Paginado",
            email="fornecedor@exemplo.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="999999999",
            data_cadastro="2023-01-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        assert id_usuario is not None
        fornecedor = Fornecedor(
            id=id_usuario,
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            cpf_cnpj=usuario.cpf_cnpj,
            telefone=usuario.telefone,
            data_cadastro=usuario.data_cadastro,
            cep=usuario.cep,
            rua=usuario.rua,
            numero=usuario.numero,
            complemento=usuario.complemento,
            bairro=usuario.bairro,
            cidade=usuario.cidade,
            estado=usuario.estado,
            razao_social="Fornecedor LTDA",
            tipo_usuario=usuario.tipo_usuario
        )
        id_fornecedor = inserir_fornecedor(fornecedor)

        nomes_anuncios = [
            "Banheiro Reformado",
            "Cozinha Planejada",
            "Quarto Decorado", 
            "Varanda Gourmet",
            "Área de Lazer"
        ]
        assert id_fornecedor is not None

        for nome in nomes_anuncios:
            anuncio = Anuncio(
                id_anuncio=0,
                nome_anuncio=nome,
                id_fornecedor=id_fornecedor,
                data_criacao="2023-01-01",
                descricao=f"Descrição para {nome}",
                preco=150.0
            )
            inserir_anuncio(anuncio)

        # Act – buscar pelo termo "Quarto"
        resultados = obter_anuncio_por_termo_paginado("Quarto", 10, 0)

        # Assert
        assert len(resultados) == 1
        assert resultados[0].nome_anuncio == "Quarto Decorado"

    def test_atualizar_anuncio_por_nome(self, test_db):
    # Arrange - preparar tabelas e dados
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@teste.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="999999999",
            data_cadastro="2023-01-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        assert id_usuario is not None
        fornecedor = Fornecedor(
            id=id_usuario,
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            cpf_cnpj=usuario.cpf_cnpj,
            telefone=usuario.telefone,
            data_cadastro=usuario.data_cadastro,
            cep=usuario.cep,
            rua=usuario.rua,
            numero=usuario.numero,
            complemento=usuario.complemento,
            bairro=usuario.bairro,
            cidade=usuario.cidade,
            estado=usuario.estado,
            razao_social="Fornecedor LTDA",
            tipo_usuario=usuario.tipo_usuario
        )
        id_fornecedor = inserir_fornecedor(fornecedor)

        assert id_fornecedor is not None
        anuncio_original = Anuncio(
            id_anuncio=0,
            nome_anuncio="Anuncio Original",
            id_fornecedor=id_fornecedor,
            data_criacao="2023-01-01",
            descricao="Descricao original",
            preco=100.0
        )
        id_anuncio = inserir_anuncio(anuncio_original)

        assert id_anuncio is not None
        # Act - atualizar o anúncio pelo nome antigo
        anuncio_atualizado = Anuncio(
            id_anuncio=id_anuncio,
            nome_anuncio="Anuncio Atualizado",
            id_fornecedor=id_fornecedor,
            data_criacao="2023-02-01",
            descricao="Descricao atualizada",
            preco=150.0
        )
        sucesso = atualizar_anuncio_por_nome(anuncio_atualizado, "Anuncio Original")

        # Assert - verificar se a atualização foi bem sucedida
        assert sucesso is True

        assert id_anuncio is not None
        anuncio_bd = obter_anuncio_por_id(id_anuncio)
        assert anuncio_bd is not None
        assert anuncio_bd.nome_anuncio == "Anuncio Atualizado"
        assert anuncio_bd.data_criacao == "2023-02-01"
        assert anuncio_bd.descricao == "Descricao atualizada"
        assert anuncio_bd.preco == 150.0


    def test_deletar_anuncio(self, test_db):
    # Arrange - preparar tabelas e dados
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_anuncio()

        usuario = Usuario(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@teste.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="999999999",
            data_cadastro="2023-01-01",
            tipo_usuario="Fornecedor",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_usuario = inserir_usuario(usuario)

        assert id_usuario is not None
        fornecedor = Fornecedor(
            id=id_usuario,
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            cpf_cnpj=usuario.cpf_cnpj,
            telefone=usuario.telefone,
            data_cadastro=usuario.data_cadastro,
            cep=usuario.cep,
            rua=usuario.rua,
            numero=usuario.numero,
            complemento=usuario.complemento,
            bairro=usuario.bairro,
            cidade=usuario.cidade,
            estado=usuario.estado,
            razao_social="Fornecedor LTDA",
            tipo_usuario=usuario.tipo_usuario
        )
        id_fornecedor = inserir_fornecedor(fornecedor)
        assert id_fornecedor is not None

        anuncio = Anuncio(
            id_anuncio=0,
            nome_anuncio="Anuncio Para Deletar",
            id_fornecedor=id_fornecedor,
            data_criacao="2023-01-01",
            descricao="Descricao teste para deletar",
            preco=100.0
        )
        id_anuncio = inserir_anuncio(anuncio)

        assert id_anuncio is not None
        # Act - deletar o anúncio
        sucesso = deletar_anuncio(id_anuncio)

        # Assert - verificar se a exclusão foi bem sucedida
        assert sucesso is True
        anuncio_bd = obter_anuncio_por_id(id_anuncio)
        assert anuncio_bd is None
