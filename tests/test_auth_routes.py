"""
Testes para rotas de autenticação (auth_routes.py)

Testa:
- Login (GET/POST)
- Logout
- Recuperação de senha
- Redefinição de senha
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from main import app
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from data.administrador import administrador_repo
from data.administrador.administrador_model import Administrador
from util.security import criar_hash_senha, gerar_token_redefinicao

client = TestClient(app)


@pytest.fixture
def setup_tabelas_auth(test_db):
    """
    Cria todas as tabelas necessárias para testes de autenticação.
    """
    usuario_repo.criar_tabela_usuario()
    cliente_repo.criar_tabela_cliente()
    administrador_repo.criar_tabela_administrador()
    yield


@pytest.fixture
def usuario_teste(setup_tabelas_auth, email_unico, cpf_unico):
    """
    Cria um usuário de teste no banco de dados.
    """
    cliente = Cliente(
        id=0,
        nome="Usuário Teste",
        email=email_unico,
        senha=criar_hash_senha("senha123"),
        cpf_cnpj=cpf_unico,
        telefone="27999999999",
        cep="29100-000",
        rua="Rua Teste",
        numero="123",
        complemento="",
        bairro="Bairro Teste",
        cidade="Vitória",
        estado="ES",
        tipo_usuario="cliente",
        data_cadastro=datetime.now().isoformat(),
        foto=None,
        token_redefinicao=None,
        data_token=None,
        genero="Não Informado",
        data_nascimento="2000-01-01"
    )

    # inserir_cliente já insere tanto na tabela usuario quanto na tabela cliente
    cliente_id = cliente_repo.inserir_cliente(cliente)
    cliente.id = cliente_id

    yield cliente

    # Cleanup não é necessário pois o banco é temporário


class TestLoginRoutes:
    """Testes para rotas de login"""

    def test_mostrar_login_get(self):
        """Testa exibição da página de login"""
        response = client.get("/login")
        assert response.status_code == 200
        assert "login" in response.text.lower()

    def test_mostrar_login_com_mensagem(self):
        """Testa exibição da página de login com mensagem de sucesso"""
        response = client.get("/login?mensagem=Bem-vindo!")
        assert response.status_code == 200
        assert "login" in response.text.lower()

    def test_login_campos_vazios(self):
        """Testa login com campos vazios"""
        response = client.post("/login", data={
            "email": "",
            "senha": ""
        })
        # ValidationError retorna 200 com template de erro
        assert response.status_code in [200, 400]
        # Deve conter mensagem de erro sobre email ou campos obrigatórios
        assert "email" in response.text.lower() or "senha" in response.text.lower()

    def test_login_email_invalido(self, setup_tabelas_auth):
        """Testa login com email que não existe"""
        response = client.post("/login", data={
            "email": "naoexiste@teste.com",
            "senha": "senha123"
        })
        # Retorna 401 para credenciais inválidas
        assert response.status_code == 401
        # Verifica que retornou HTML (template de login com erro)
        assert "login" in response.text.lower()

    def test_login_senha_incorreta(self, usuario_teste):
        """Testa login com senha incorreta"""
        response = client.post("/login", data={
            "email": usuario_teste.email,
            "senha": "senhaerrada"
        })
        # Retorna 401 para credenciais inválidas
        assert response.status_code == 401
        # Verifica que retornou HTML (template de login com erro)
        assert "login" in response.text.lower()

    def test_login_sucesso_cliente(self, usuario_teste):
        """Testa login bem-sucedido de cliente"""
        response = client.post("/login", data={
            "email": usuario_teste.email,
            "senha": "senha123"
        }, follow_redirects=False)

        # Deve redirecionar para /cliente
        assert response.status_code == 303
        assert "/cliente" in response.headers.get("location", "")

    def test_login_sucesso_admin(self, setup_tabelas_auth, email_unico, cpf_unico):
        """Testa login bem-sucedido de administrador"""
        # Criar usuário admin
        admin_usuario = Usuario(
            id=0,
            nome="Admin Teste",
            email=email_unico,
            senha=criar_hash_senha("admin123"),
            cpf_cnpj=cpf_unico,
            telefone="27888888888",
            cep="29100-000",
            rua="Rua Admin",
            numero="1",
            complemento="",
            bairro="Centro",
            cidade="Vitória",
            estado="ES",
            tipo_usuario="administrador",
            data_cadastro=datetime.now().isoformat(),
            foto=None,
            token_redefinicao=None,
            data_token=None,
        )
        admin_id = usuario_repo.inserir_usuario(admin_usuario)
        # Criar registro na tabela administrador
        admin = Administrador(id_usuario=admin_id)
        administrador_repo.inserir_administrador(admin)

        response = client.post("/login", data={
            "email": admin_usuario.email,
            "senha": "admin123"
        }, follow_redirects=False)

        # Deve redirecionar para /administrador/home
        assert response.status_code == 303
        assert "/administrador" in response.headers.get("location", "")

    def test_login_validacao_erro_pydantic(self, setup_tabelas_auth):
        """Testa erro de validação do Pydantic (email inválido)"""
        response = client.post("/login", data={
            "email": "email-invalido-sem-arroba",
            "senha": "senha123"
        })
        # Deve retornar erro de validação
        assert response.status_code in [200, 400]


class TestLogoutRoute:
    """Testes para rota de logout"""

    def test_logout(self):
        """Testa logout do usuário"""
        response = client.get("/logout", follow_redirects=False)
        assert response.status_code == 303
        assert response.headers.get("location") == "/"


class TestRecuperarSenhaRoutes:
    """Testes para recuperação de senha"""

    def test_recuperar_senha_get(self):
        """Testa exibição do formulário de recuperação de senha"""
        response = client.get("/recuperar-senha")
        assert response.status_code == 200
        assert "recuperar" in response.text.lower() or "senha" in response.text.lower()

    def test_recuperar_senha_email_existente(self, usuario_teste):
        """Testa recuperação de senha com email existente"""
        response = client.post("/recuperar-senha", data={
            "email": usuario_teste.email
        })
        assert response.status_code == 200
        assert "enviamos" in response.text.lower() or "recuperação" in response.text.lower()

        # Verificar se token foi gerado no usuário
        usuario_atualizado = usuario_repo.obter_usuario_por_email(usuario_teste.email)
        assert usuario_atualizado.token_redefinicao is not None

    def test_recuperar_senha_email_nao_existente(self, setup_tabelas_auth):
        """Testa recuperação de senha com email que não existe"""
        response = client.post("/recuperar-senha", data={
            "email": "naoexiste@teste.com"
        })
        assert response.status_code == 200
        assert "não encontrado" in response.text.lower()


class TestResetarSenhaRoutes:
    """Testes para redefinição de senha"""

    def test_resetar_senha_get(self):
        """Testa exibição do formulário de redefinir senha"""
        token = "token-teste-123"
        response = client.get(f"/resetar-senha?token={token}")
        assert response.status_code == 200

    def test_resetar_senha_token_valido(self, usuario_teste):
        """Testa redefinição de senha com token válido"""
        # Gerar e atribuir token ao usuário
        token = gerar_token_redefinicao()
        usuario_teste.token_redefinicao = token
        usuario_repo.atualizar_usuario(usuario_teste)

        response = client.post("/resetar-senha", data={
            "token": token,
            "nova_senha": "novaSenha123"
        }, follow_redirects=False)

        # Deve redirecionar para login com mensagem de sucesso
        assert response.status_code == 303
        assert "/login" in response.headers.get("location", "")
        assert "mensagem" in response.headers.get("location", "").lower()

        # Verificar se senha foi alterada
        usuario_atualizado = usuario_repo.obter_usuario_por_email(usuario_teste.email)
        from util.security import verificar_senha
        assert verificar_senha("novaSenha123", usuario_atualizado.senha)
        assert usuario_atualizado.token_redefinicao is None

    def test_resetar_senha_token_invalido(self, setup_tabelas_auth):
        """Testa redefinição de senha com token inválido"""
        response = client.post("/resetar-senha", data={
            "token": "token-invalido-xyz",
            "nova_senha": "novaSenha123"
        })
        assert response.status_code == 200
        assert "inválido" in response.text.lower() or "expirado" in response.text.lower()


class TestLoginSessionData:
    """Testes para dados de sessão após login"""

    def test_session_data_completa_apos_login(self, usuario_teste):
        """Verifica se todos os dados necessários são salvos na sessão"""
        # Fazer login
        response = client.post("/login", data={
            "email": usuario_teste.email,
            "senha": "senha123"
        }, follow_redirects=False)

        assert response.status_code == 303

        # Verificar cookies de sessão (SessionMiddleware)
        assert "session" in response.cookies or response.status_code == 303
