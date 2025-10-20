#!/usr/bin/env python3
"""
Script de População do Banco de Dados - Projeto OBRATTO

Este script cria dados de teste realistas para o ambiente de desenvolvimento.

TODO ALUNOS: Entender o fluxo de criação de usuários
1. Por que usamos DTOs para validação antes de inserir?
2. Como as senhas são protegidas (hash)?
3. Por que criar usuários de teste é importante?
4. Como funciona a integração entre tabelas (Usuario -> Cliente/Prestador/Fornecedor)?

Uso: python scripts/popular_banco.py

IMPORTANTE: Este script NÃO deve ser executado em produção!
Use apenas em ambiente de desenvolvimento/teste.
"""

import sys
import os
from datetime import datetime, date
from typing import Optional, TypedDict

# Adicionar o diretório pai ao sys.path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.dirname(script_dir)
sys.path.insert(0, projeto_dir)

from util.security import criar_hash_senha
from util.seed import criar_tabelas
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from data.administrador import administrador_repo
from data.administrador.administrador_model import Administrador
from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from data.prestador import prestador_repo
from data.prestador.prestador_model import Prestador
from data.fornecedor import fornecedor_repo
from data.fornecedor.fornecedor_model import Fornecedor
from data.produto import produto_repo
from data.produto.produto_model import Produto
from data.plano import plano_repo
from data.plano.plano_model import Plano

# ==============================================================================
# TYPE DEFINITIONS
# ==============================================================================

class ClienteData(TypedDict):
    """Tipo para dados de cliente"""
    nome: str
    email: str
    cpf_cnpj: str
    telefone: str
    genero: str
    data_nascimento: date
    cidade: str

class ProdutoData(TypedDict):
    """Tipo para dados de produto"""
    nome: str
    descricao: str
    preco: float
    quantidade: int

class PlanoData(TypedDict):
    """Tipo para dados de plano"""
    nome: str
    descricao: str
    valor_mensal: float
    limite_servico: int
    tipo_plano: str

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================

# Senha padrão para TODOS os usuários de teste (use senha forte!)
SENHA_PADRAO = "Senha@123"

# Configuração de exibição
EMOJI_SUCESSO = "✅"
EMOJI_INFO = "ℹ️"
EMOJI_ALERTA = "⚠️"
EMOJI_ERRO = "❌"
EMOJI_SETA = "➜"

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def print_header(titulo: str):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f"  {titulo}")
    print("=" * 80)


def print_sucesso(mensagem: str):
    """Imprime mensagem de sucesso"""
    print(f"{EMOJI_SUCESSO} {mensagem}")


def print_info(mensagem: str):
    """Imprime mensagem informativa"""
    print(f"{EMOJI_INFO} {mensagem}")


def print_alerta(mensagem: str):
    """Imprime mensagem de alerta"""
    print(f"{EMOJI_ALERTA} {mensagem}")


def print_erro(mensagem: str):
    """Imprime mensagem de erro"""
    print(f"{EMOJI_ERRO} {mensagem}")


def criar_usuario_base(
    nome: str,
    email: str,
    cpf_cnpj: str,
    telefone: str,
    tipo_usuario: str,
    cep: str = "29000-000",
    rua: str = "Rua Exemplo",
    numero: str = "100",
    bairro: str = "Centro",
    cidade: str = "Vitória",
    estado: str = "ES",
    complemento: str = "",
    foto: Optional[str] = None
) -> Optional[int]:
    """
    Cria um usuário na tabela base 'usuario'

    TODO ALUNOS: Esta função demonstra:
    - Criação de hash seguro de senha
    - Estrutura do modelo Usuario
    - Inserção usando Repository Pattern

    Retorna: ID do usuário criado ou None em caso de erro
    """
    try:
        senha_hash = criar_hash_senha(SENHA_PADRAO)

        usuario = Usuario(
            id=0,  # Será gerado automaticamente pelo banco
            nome=nome,
            email=email,
            senha=senha_hash,
            cpf_cnpj=cpf_cnpj,
            telefone=telefone,
            cep=cep,
            rua=rua,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            tipo_usuario=tipo_usuario,
            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            foto=foto,
            token_redefinicao=None,
            data_token=None,
        )

        id_usuario = usuario_repo.inserir_usuario(usuario)
        return id_usuario
    except Exception as e:
        print_erro(f"Erro ao criar usuário {email}: {e}")
        return None


# ==============================================================================
# CRIAÇÃO DE ADMINISTRADORES
# ==============================================================================

def criar_administradores():
    """
    Cria 3 administradores de teste

    TODO ALUNOS: Observe que:
    1. Admin é criado em 2 etapas: Usuario + Administrador
    2. A tabela 'administrador' só guarda id_usuario (chave estrangeira)
    3. Todos os dados pessoais ficam na tabela 'usuario'
    """
    print_header("CRIANDO ADMINISTRADORES")

    admins = [
        {
            "nome": "Admin Principal",
            "email": "admin@obratto.com",
            "cpf_cnpj": "111.111.111-11",
            "telefone": "(27) 99999-0001",
        },
        {
            "nome": "Maria Administradora",
            "email": "maria.admin@obratto.com",
            "cpf_cnpj": "222.222.222-22",
            "telefone": "(27) 99999-0002",
        },
        {
            "nome": "João Moderador",
            "email": "joao.admin@obratto.com",
            "cpf_cnpj": "333.333.333-33",
            "telefone": "(27) 99999-0003",
        },
    ]

    for admin_data in admins:
        # Verifica se já existe
        usuario_existente = usuario_repo.obter_usuario_por_email(admin_data["email"])
        if usuario_existente:
            print_info(f"Admin já existe: {admin_data['email']}")
            continue

        # Cria usuário base
        id_usuario = criar_usuario_base(
            nome=admin_data["nome"],
            email=admin_data["email"],
            cpf_cnpj=admin_data["cpf_cnpj"],
            telefone=admin_data["telefone"],
            tipo_usuario="Administrador",
        )

        if id_usuario:
            # Cria registro específico de administrador
            administrador = Administrador(id=None, id_usuario=id_usuario)
            admin_id = administrador_repo.inserir_administrador(administrador)

            if admin_id:
                print_sucesso(f"Admin criado: {admin_data['email']}")
                print(f"  {EMOJI_SETA} Nome: {admin_data['nome']}")
                print(f"  {EMOJI_SETA} Senha: {SENHA_PADRAO}")
            else:
                print_erro(f"Erro ao criar registro de administrador para {admin_data['email']}")
        else:
            print_erro(f"Erro ao criar usuário base para {admin_data['email']}")


# ==============================================================================
# CRIAÇÃO DE CLIENTES
# ==============================================================================

def criar_clientes():
    """
    Cria 5 clientes de teste com perfis diversos

    TODO ALUNOS: Observe:
    - Diversidade de dados (gêneros, idades, localizações)
    - Campo 'genero' e 'data_nascimento' específicos de Cliente
    - Por que ter dados variados ajuda nos testes?
    """
    print_header("CRIANDO CLIENTES")

    clientes: list[ClienteData] = [
        {
            "nome": "Maria Silva",
            "email": "maria.silva@teste.com",
            "cpf_cnpj": "444.444.444-44",
            "telefone": "(27) 98888-0001",
            "genero": "Feminino",
            "data_nascimento": date(1990, 5, 15),
            "cidade": "Vitória",
        },
        {
            "nome": "João Santos",
            "email": "joao.santos@teste.com",
            "cpf_cnpj": "555.555.555-55",
            "telefone": "(27) 98888-0002",
            "genero": "Masculino",
            "data_nascimento": date(1985, 8, 22),
            "cidade": "Vila Velha",
        },
        {
            "nome": "Ana Paula Costa",
            "email": "ana.costa@teste.com",
            "cpf_cnpj": "666.666.666-66",
            "telefone": "(27) 98888-0003",
            "genero": "Feminino",
            "data_nascimento": date(1995, 3, 10),
            "cidade": "Serra",
        },
        {
            "nome": "Carlos Eduardo Lima",
            "email": "carlos.lima@teste.com",
            "cpf_cnpj": "777.777.777-77",
            "telefone": "(27) 98888-0004",
            "genero": "Masculino",
            "data_nascimento": date(1988, 12, 5),
            "cidade": "Cariacica",
        },
        {
            "nome": "Fernanda Oliveira",
            "email": "fernanda.oliveira@teste.com",
            "cpf_cnpj": "888.888.888-88",
            "telefone": "(27) 98888-0005",
            "genero": "Feminino",
            "data_nascimento": date(1992, 7, 18),
            "cidade": "Vitória",
        },
    ]

    for cliente_data in clientes:
        # Verifica se já existe
        email: str = cliente_data["email"]
        usuario_existente = usuario_repo.obter_usuario_por_email(email)
        if usuario_existente:
            print_info(f"Cliente já existe: {cliente_data['email']}")
            continue

        # Cria cliente diretamente (já inclui criação na tabela usuario)
        cliente = Cliente(
            id=0,
            nome=cliente_data["nome"],
            email=cliente_data["email"],
            senha=criar_hash_senha(SENHA_PADRAO),
            cpf_cnpj=cliente_data["cpf_cnpj"],
            telefone=cliente_data["telefone"],
            cep="29000-000",
            estado="ES",
            cidade=cliente_data["cidade"],
            rua="Rua Exemplo",
            numero="100",
            complemento="",
            bairro="Centro",
            tipo_usuario="Cliente",
            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            foto=None,
            token_redefinicao=None,
            data_token=None,
            genero=cliente_data["genero"],
            data_nascimento=cliente_data["data_nascimento"],
        )

        cliente_id = cliente_repo.inserir_cliente(cliente)

        if cliente_id:
            print_sucesso(f"Cliente criado: {cliente_data['email']}")
            print(f"  {EMOJI_SETA} Nome: {cliente_data['nome']}")
            print(f"  {EMOJI_SETA} Gênero: {cliente_data['genero']}")
            print(f"  {EMOJI_SETA} Senha: {SENHA_PADRAO}")
        else:
            print_erro(f"Erro ao criar cliente {cliente_data['email']}")


# ==============================================================================
# CRIAÇÃO DE PRESTADORES
# ==============================================================================

def criar_prestadores():
    """
    Cria 5 prestadores de teste com diferentes áreas de atuação

    TODO ALUNOS: Observe:
    - Campos específicos: area_atuacao, razao_social, descricao_servicos
    - Diversidade de profissionais
    - Como isso simula um ambiente real
    """
    print_header("CRIANDO PRESTADORES")

    prestadores = [
        {
            "nome": "Pedro Eletricista",
            "email": "pedro.eletricista@teste.com",
            "cpf_cnpj": "101.101.101-01",
            "telefone": "(27) 97777-0001",
            "area_atuacao": "Elétrica",
            "razao_social": "Pedro Elétrica MEI",
            "descricao_servicos": "Instalações elétricas residenciais e comerciais, manutenção preventiva e corretiva.",
        },
        {
            "nome": "Carla Encanadora",
            "email": "carla.encanadora@teste.com",
            "cpf_cnpj": "202.202.202-02",
            "telefone": "(27) 97777-0002",
            "area_atuacao": "Hidráulica",
            "razao_social": "Carla Hidráulica",
            "descricao_servicos": "Instalação e reparo de sistemas hidráulicos, desentupimento, troca de encanamentos.",
        },
        {
            "nome": "Ricardo Pintor",
            "email": "ricardo.pintor@teste.com",
            "cpf_cnpj": "303.303.303-03",
            "telefone": "(27) 97777-0003",
            "area_atuacao": "Pintura",
            "razao_social": "Ricardo Pinturas",
            "descricao_servicos": "Pintura residencial e comercial, textura, grafiato, lavagem de paredes.",
        },
        {
            "nome": "Julia Jardineira",
            "email": "julia.jardineira@teste.com",
            "cpf_cnpj": "404.404.404-04",
            "telefone": "(27) 97777-0004",
            "area_atuacao": "Jardinagem",
            "razao_social": "Julia Jardins",
            "descricao_servicos": "Paisagismo, manutenção de jardins, poda de árvores, plantio de grama.",
        },
        {
            "nome": "Marcos Pedreiro",
            "email": "marcos.pedreiro@teste.com",
            "cpf_cnpj": "505.505.505-05",
            "telefone": "(27) 97777-0005",
            "area_atuacao": "Construção Civil",
            "razao_social": "Marcos Construções",
            "descricao_servicos": "Alvenaria, reboco, contrapiso, pequenas reformas, muros.",
        },
    ]

    for prestador_data in prestadores:
        # Verifica se já existe
        usuario_existente = usuario_repo.obter_usuario_por_email(prestador_data["email"])
        if usuario_existente:
            print_info(f"Prestador já existe: {prestador_data['email']}")
            continue

        # Cria prestador
        prestador = Prestador(
            id=0,
            nome=prestador_data["nome"],
            email=prestador_data["email"],
            senha=criar_hash_senha(SENHA_PADRAO),
            cpf_cnpj=prestador_data["cpf_cnpj"],
            telefone=prestador_data["telefone"],
            cep="29000-000",
            estado="ES",
            cidade="Vitória",
            rua="Rua Exemplo",
            numero="100",
            complemento="",
            bairro="Centro",
            tipo_usuario="Prestador",
            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            foto=None,
            token_redefinicao=None,
            data_token=None,
            area_atuacao=prestador_data["area_atuacao"],
            razao_social=prestador_data["razao_social"],
            descricao_servicos=prestador_data["descricao_servicos"],
        )

        prestador_id = prestador_repo.inserir_prestador(prestador)

        if prestador_id:
            print_sucesso(f"Prestador criado: {prestador_data['email']}")
            print(f"  {EMOJI_SETA} Nome: {prestador_data['nome']}")
            print(f"  {EMOJI_SETA} Área: {prestador_data['area_atuacao']}")
            print(f"  {EMOJI_SETA} Senha: {SENHA_PADRAO}")
        else:
            print_erro(f"Erro ao criar prestador {prestador_data['email']}")


# ==============================================================================
# CRIAÇÃO DE FORNECEDORES
# ==============================================================================

def criar_fornecedores():
    """
    Cria 5 fornecedores de teste

    TODO ALUNOS: Observe:
    - Uso de CNPJ (formato diferente de CPF)
    - Campo razao_social obrigatório
    - Diferentes segmentos de mercado
    """
    print_header("CRIANDO FORNECEDORES")

    fornecedores = [
        {
            "nome": "Casa das Tintas",
            "email": "contato@casadastintas.com",
            "cpf_cnpj": "11.111.111/0001-11",
            "telefone": "(27) 3333-0001",
            "razao_social": "Casa das Tintas Ltda",
        },
        {
            "nome": "Materiais Hidráulicos Silva",
            "email": "vendas@materiaissilva.com",
            "cpf_cnpj": "22.222.222/0001-22",
            "telefone": "(27) 3333-0002",
            "razao_social": "Silva Materiais Hidráulicos Ltda",
        },
        {
            "nome": "Elétrica Total",
            "email": "contato@eletricatotal.com",
            "cpf_cnpj": "33.333.333/0001-33",
            "telefone": "(27) 3333-0003",
            "razao_social": "Elétrica Total Comercial Ltda",
        },
        {
            "nome": "Jardinagem Verde Vida",
            "email": "vendas@verdevida.com",
            "cpf_cnpj": "44.444.444/0001-44",
            "telefone": "(27) 3333-0004",
            "razao_social": "Verde Vida Jardinagem e Paisagismo Ltda",
        },
        {
            "nome": "Construção Forte",
            "email": "comercial@construcaoforte.com",
            "cpf_cnpj": "55.555.555/0001-55",
            "telefone": "(27) 3333-0005",
            "razao_social": "Construção Forte Materiais de Construção Ltda",
        },
    ]

    for fornecedor_data in fornecedores:
        # Verifica se já existe
        usuario_existente = usuario_repo.obter_usuario_por_email(fornecedor_data["email"])
        if usuario_existente:
            print_info(f"Fornecedor já existe: {fornecedor_data['email']}")
            continue

        # Cria fornecedor
        fornecedor = Fornecedor(
            id=0,
            nome=fornecedor_data["nome"],
            email=fornecedor_data["email"],
            senha=criar_hash_senha(SENHA_PADRAO),
            cpf_cnpj=fornecedor_data["cpf_cnpj"],
            telefone=fornecedor_data["telefone"],
            cep="29000-000",
            estado="ES",
            cidade="Vitória",
            rua="Rua Exemplo",
            numero="100",
            complemento="Loja",
            bairro="Centro",
            tipo_usuario="Fornecedor",
            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            foto=None,
            token_redefinicao=None,
            data_token=None,
            razao_social=fornecedor_data["razao_social"],
        )

        fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)

        if fornecedor_id:
            print_sucesso(f"Fornecedor criado: {fornecedor_data['email']}")
            print(f"  {EMOJI_SETA} Razão Social: {fornecedor_data['razao_social']}")
            print(f"  {EMOJI_SETA} Senha: {SENHA_PADRAO}")
        else:
            print_erro(f"Erro ao criar fornecedor {fornecedor_data['email']}")


# ==============================================================================
# CRIAÇÃO DE PRODUTOS (Para cada fornecedor)
# ==============================================================================

def criar_produtos():
    """
    Cria produtos para cada fornecedor

    TODO ALUNOS: Observe:
    - Relação Fornecedor -> Produtos (1:N)
    - Como buscar fornecedor por email
    - Importância de dados relacionados para testes
    """
    print_header("CRIANDO PRODUTOS")

    # Produtos por fornecedor
    produtos_por_fornecedor: dict[str, list[ProdutoData]] = {
        "contato@casadastintas.com": [
            {"nome": "Tinta Acrílica Branca 18L", "descricao": "Tinta acrílica premium para interiores e exteriores", "preco": 189.90, "quantidade": 50},
            {"nome": "Tinta Látex Amarela 3.6L", "descricao": "Tinta látex lavável para paredes internas", "preco": 45.90, "quantidade": 100},
            {"nome": "Verniz Marítimo 900ml", "descricao": "Verniz protetor para madeiras expostas", "preco": 67.50, "quantidade": 30},
        ],
        "vendas@materiaissilva.com": [
            {"nome": "Registro de Pressão 1/2", "descricao": "Registro esfera metálico alta pressão", "preco": 28.90, "quantidade": 150},
            {"nome": "Caixa D'água 1000L", "descricao": "Caixa d'água polietileno com tampa", "preco": 320.00, "quantidade": 20},
            {"nome": "Tubo PVC 50mm 6m", "descricao": "Tubo PVC esgoto série normal", "preco": 42.50, "quantidade": 80},
        ],
        "contato@eletricatotal.com": [
            {"nome": "Disjuntor Bipolar 40A", "descricao": "Disjuntor termomagnético DIN", "preco": 35.90, "quantidade": 100},
            {"nome": "Tomada 2P+T 10A Branca", "descricao": "Tomada padrão brasileiro com terra", "preco": 8.50, "quantidade": 200},
            {"nome": "Fio Flexível 2.5mm 100m", "descricao": "Cabo flexível para instalações elétricas", "preco": 120.00, "quantidade": 50},
        ],
        "vendas@verdevida.com": [
            {"nome": "Substrato Orgânico 15kg", "descricao": "Terra adubada para plantio", "preco": 22.90, "quantidade": 100},
            {"nome": "Grama Esmeralda m²", "descricao": "Grama natural em placas", "preco": 8.00, "quantidade": 500},
            {"nome": "Kit Ferramentas Jardinagem", "descricao": "Kit completo com pá, rastelo e tesoura", "preco": 89.90, "quantidade": 30},
        ],
        "comercial@construcaoforte.com": [
            {"nome": "Cimento CP-II 50kg", "descricao": "Cimento Portland composto", "preco": 32.50, "quantidade": 200},
            {"nome": "Areia Média m³", "descricao": "Areia lavada para construção", "preco": 85.00, "quantidade": 50},
            {"nome": "Tijolo Furado 8 Furos", "descricao": "Tijolo cerâmico vermelho", "preco": 0.65, "quantidade": 5000},
        ],
    }

    for email_fornecedor, produtos in produtos_por_fornecedor.items():
        # Busca fornecedor
        fornecedor = fornecedor_repo.obter_fornecedor_por_email(email_fornecedor)
        if not fornecedor:
            print_alerta(f"Fornecedor não encontrado: {email_fornecedor}")
            continue

        for produto_data in produtos:
            produto = Produto(
                id=None,
                nome=produto_data["nome"],
                descricao=produto_data["descricao"],
                preco=produto_data["preco"],
                quantidade=produto_data["quantidade"],
                foto=None,  # TODO: Adicionar fotos de produtos
                fornecedor_id=fornecedor.id,
            )

            try:
                produto_id = produto_repo.inserir_produto(produto)

                if produto_id:
                    print_sucesso(f"Produto criado: {produto_data['nome']}")
                    print(f"  {EMOJI_SETA} Fornecedor: {fornecedor.nome}")
                    print(f"  {EMOJI_SETA} Preço: R$ {produto_data['preco']:.2f}")
                else:
                    print_erro(f"Erro ao criar produto {produto_data['nome']}")
            except Exception as e:
                print_erro(f"Erro ao criar produto {produto_data['nome']}: {e}")


# ==============================================================================
# CRIAÇÃO DE PLANOS
# ==============================================================================

def criar_planos():
    """
    Cria planos de assinatura (Básico, Padrão, Premium)

    TODO ALUNOS: Observe:
    - Estrutura de planos de negócio
    - Diferentes benefícios por nível
    - Como isso suporta o modelo de receita do sistema
    """
    print_header("CRIANDO PLANOS")

    planos: list[PlanoData] = [
        {
            "nome": "Básico",
            "descricao": "Plano ideal para quem está começando",
            "valor_mensal": 29.90,
            "limite_servico": 10,
            "tipo_plano": "Básico",
        },
        {
            "nome": "Padrão",
            "descricao": "Plano recomendado para profissionais",
            "valor_mensal": 59.90,
            "limite_servico": 50,
            "tipo_plano": "Padrão",
        },
        {
            "nome": "Premium",
            "descricao": "Plano completo para empresas",
            "valor_mensal": 99.90,
            "limite_servico": 999,
            "tipo_plano": "Premium",
        },
    ]

    for plano_data in planos:
        # Verifica se já existe
        plano_existente = plano_repo.obter_plano_por_nome(plano_data["nome"])
        if plano_existente:
            print_info(f"Plano já existe: {plano_data['nome']}")
            continue

        plano = Plano(
            id_plano=None,
            nome_plano=plano_data["nome"],  # Campo correto: nome_plano
            descricao=plano_data["descricao"],
            valor_mensal=plano_data["valor_mensal"],
            limite_servico=plano_data["limite_servico"],  # Campo obrigatório
            tipo_plano=plano_data["tipo_plano"],  # Campo obrigatório
        )

        plano_id = plano_repo.inserir_plano(plano)

        if plano_id:
            print_sucesso(f"Plano criado: {plano_data['nome']}")
            print(f"  {EMOJI_SETA} Valor mensal: R$ {plano_data['valor_mensal']:.2f}")
        else:
            print_erro(f"Erro ao criar plano {plano_data['nome']}")


# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

def main():
    """
    Função principal que executa todo o processo de população

    TODO ALUNOS: Observe a ordem de criação:
    1. Criar tabelas (se não existirem)
    2. Criar usuários independentes (Admin, Cliente)
    3. Criar usuários com dependências (Prestador, Fornecedor)
    4. Criar dados relacionados (Produtos, Planos)

    Por que essa ordem é importante?
    - Evita erros de chave estrangeira
    - Garante integridade referencial
    """
    print("\n")
    print("=" * 80)
    print("  🌱 POPULAÇÃO DO BANCO DE DADOS - PROJETO OBRATTO")
    print("=" * 80)
    print(f"\n{EMOJI_ALERTA} ATENÇÃO: Use apenas em ambiente de desenvolvimento!")
    print(f"{EMOJI_INFO} Senha padrão para TODOS os usuários: {SENHA_PADRAO}\n")

    try:
        # 1. Criar tabelas (se não existirem)
        print_info("Criando/verificando estrutura de tabelas...")
        criar_tabelas()
        print_sucesso("Tabelas verificadas!\n")

        # 2. Criar usuários
        criar_administradores()
        criar_clientes()
        criar_prestadores()
        criar_fornecedores()

        # 3. Criar dados relacionados
        criar_produtos()
        criar_planos()

        # 4. Resumo final
        print_header("RESUMO DA POPULAÇÃO")

        total_usuarios = len(usuario_repo.obter_usuarios_por_pagina(1, 1000))  # (pagina, tamanho)
        total_produtos = len(produto_repo.obter_produto_por_pagina(1000, 0))  # (limit, offset)
        total_planos = len(plano_repo.obter_plano_por_pagina(1, 1000))  # (pagina, tamanho)

        print(f"\n{EMOJI_SUCESSO} População concluída com sucesso!\n")
        print(f"  📊 Total de usuários criados: {total_usuarios}")
        print(f"  📦 Total de produtos criados: {total_produtos}")
        print(f"  💎 Total de planos criados: {total_planos}")
        print(f"\n  🔑 Senha padrão: {SENHA_PADRAO}")
        print(f"  {EMOJI_ALERTA} Lembre-se de alterar as senhas em produção!\n")

        print("=" * 80)
        print("  ✨ BANCO DE DADOS PRONTO PARA USO!")
        print("=" * 80)
        print("\n  📝 Próximos passos:")
        print(f"  {EMOJI_SETA} Inicie o servidor: uvicorn main:app --reload")
        print(f"  {EMOJI_SETA} Acesse: http://localhost:8000")
        print(f"  {EMOJI_SETA} Faça login com qualquer usuário criado\n")

    except Exception as e:
        print_erro(f"\nErro durante a população do banco: {e}")
        import traceback
        print(traceback.format_exc())
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
