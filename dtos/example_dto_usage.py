from datetime import date, datetime
from pydantic import ValidationError

from data.usuario.usuario_model import Usuario
from data.cliente.cliente_model import Cliente
from data.prestador.prestador_model import Prestador
from data.servico.servico_model import Servico
from data.anuncio.anuncio_model import Anuncio
from data.avaliacao.avaliacao_model import Avaliacao
from data.mensagem.mensagem_model import Mensagem
from data.orcamento.orcamento_model import Orcamento
from data.orcamentoservico.orcamento_servico_model import OrcamentoServico
from data.notificacao.notificacao_model import Notificacao

from dtos.usuario.usuario_dto import UsuarioDTO
from dtos.cliente.cliente_dto import  CriarClienteDTO, AtualizarClienteDTO
from dtos.prestador.prestador_dto import CriarPrestadorDTO, AtualizarPrestadorDTO
from dtos.prestador.servico_dto import CriarServicoDTO, AtualizarServicoDTO
from dtos.usuario.avaliacao_dto import CriarAvaliacaoDTO, AtualizarAvaliacaoDTO
from dtos.usuario.mensagem_dto import CriarMensagemDTO, AtualizarMensagemDTO
from dtos.usuario.orcamento_servico_dto import  CriarOrcamentoServicoDTO, AtualizarOrcamentoServicoDTO
from dtos.usuario.notificacao_dto import CriarNotificacaoDTO, AtualizarNotificacaoDTO

# Exemplo de uso para Cliente
def exemplo_cliente_dto_pydantic():
    print("--- Exemplo de Cliente e ClienteDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo Cliente (dataclass original)
    cliente_model = Cliente(
        id=1,
        nome="João Silva",
        email="joao.silva@example.com",
        senha="senha123",
        cpf_cnpj="111.222.333-44",
        telefone="(11) 98765-4321",
        cep="01000-000",
        rua="Rua Exemplo",
        numero="123",
        complemento="Apto 101",
        bairro="Centro",
        cidade="São Paulo",
        estado="SP",
        tipo_usuario="cliente",
        data_cadastro="2023-01-15",
        foto="url_foto_joao.jpg",
        genero="Masculino",
        data_nascimento=date(1990, 5, 20)
    )
    print(f"Modelo Cliente (dataclass): {cliente_model}")

    # 2. Converter o modelo Cliente para ClienteDTO (Pydantic)
    # Pydantic pode converter diretamente de objetos com atributos compatíveis
    cliente_dto = CriarClienteDTO.model_validate(cliente_model)
    print(f"ClienteDTO (convertido do modelo): {cliente_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarClienteDTO diretamente (ex: recebido de um formulário/API para criação)
    criar_cliente_dto = CriarClienteDTO(
        nome="Ana Paula",
        email="ana.paula@example.com",
        senha="nova_senha456",
        cpf_cnpj="555.666.777-88",
        telefone="(21) 98765-1234",
        cep="20000-000",
        rua="Av. Atlântica",
        numero="1000",
        bairro="Copacabana",
        cidade="Rio de Janeiro",
        estado="RJ",
        genero="Feminino",
        data_nascimento=date(1992, 3, 15)
    )
    print(f"CriarClienteDTO (criado diretamente): {criar_cliente_dto.model_dump_json(indent=2)}")

    # 4. Criar um AtualizarClienteDTO (ex: recebido de um formulário/API para atualização)
    atualizar_cliente_dto = AtualizarClienteDTO(
        email="ana.paula.novo@example.com",
        telefone="(21) 99999-8888"
    )
    print(f"AtualizarClienteDTO (criado diretamente): {atualizar_cliente_dto.model_dump_json(indent=2)}")

    # 5. Exemplo de como usar os dados do DTO
    print(f"Nome do CriarClienteDTO: {criar_cliente_dto.nome}")
    print(f"Email do AtualizarClienteDTO: {atualizar_cliente_dto.email}")


# Exemplo de uso para Prestador
def exemplo_prestador_dto_pydantic():
    print("\n--- Exemplo de Prestador e PrestadorDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo Prestador (dataclass original)
    prestador_model = Prestador(
        id=101,
        nome="Serviços Rápidos Ltda.",
        email="contato@servicosrapidos.com",
        senha="senha456",
        cpf_cnpj="12.345.678/0001-90",
        telefone="(21) 99887-6655",
        cep="20000-000",
        rua="Av. Principal",
        numero="500",
        complemento="Sala 10",
        bairro="Centro",
        cidade="Rio de Janeiro",
        estado="RJ",
        tipo_usuario="prestador",
        data_cadastro="2022-03-01",
        foto="url_foto_empresa.jpg",
        area_atuacao="Reformas e Construção",
        razao_social="Serviços Rápidos Ltda.",
        descricao_servicos="Especialistas em reformas residenciais e comerciais.",
        selo_confianca=True
    )
    print(f"Modelo Prestador (dataclass): {prestador_model}")

    # 2. Converter o modelo Prestador para PrestadorDTO (Pydantic)
    prestador_dto = CriarPrestadorDTO.model_validate(prestador_model)
    print(f"PrestadorDTO (convertido do modelo): {prestador_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarPrestadorDTO diretamente
    criar_prestador_dto = CriarPrestadorDTO(
        nome="Eletricista Confiável",
        email="contato@eletricistaconfiavel.com",
        senha="segura123",
        cpf_cnpj="11.222.333/0001-44",
        telefone="(11) 98765-4321",
        cep="04545-000",
        rua="Rua do Eletricista",
        numero="50",
        bairro="Vila Olímpia",
        cidade="São Paulo",
        estado="SP",
        area_atuacao="Eletricidade",
        descricao_servicos="Instalações e reparos elétricos em geral."
    )
    print(f"CriarPrestadorDTO (criado diretamente): {criar_prestador_dto.model_dump_json(indent=2)}")

    # 4. Criar um AtualizarPrestadorDTO
    atualizar_prestador_dto = AtualizarPrestadorDTO(
        descricao_servicos="Instalações, reparos e manutenção preventiva.",
        selo_confianca=True
    )
    print(f"AtualizarPrestadorDTO (criado diretamente): {atualizar_prestador_dto.model_dump_json(indent=2)}")

    # 5. Exemplo de como usar os dados do DTO
    print(f"Nome do CriarPrestadorDTO: {criar_prestador_dto.nome}")
    print(f"Descrição do AtualizarPrestadorDTO: {atualizar_prestador_dto.descricao_servicos}")


# Exemplo de uso para Servico
def exemplo_servico_dto_pydantic():
    print("\n--- Exemplo de Servico e ServicoDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo Servico (dataclass original)
    servico_model = Servico(
        id_servico=1,
        id_prestador=101,
        titulo="Instalação Elétrica Residencial",
        descricao="Instalação completa de fiação e tomadas em residências.",
        categoria="Eletricidade",
        valor_base=250.00,
        nome_prestador="Eletricista Confiável"
    )
    print(f"Modelo Servico (dataclass): {servico_model}")

    # 2. Converter o modelo Servico para ServicoDTO (Pydantic)
    servico_dto = CriarServicoDTO.model_validate(servico_model)
    print(f"ServicoDTO (convertido do modelo): {servico_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarServicoDTO diretamente
    criar_servico_dto = CriarServicoDTO(
        id_prestador=101,
        titulo="Manutenção de Ar Condicionado",
        descricao="Limpeza e verificação de sistemas de ar condicionado para residências e escritórios.",
        categoria="Refrigeração",
        valor_base=180.50
    )
    print(f"CriarServicoDTO (criado diretamente): {criar_servico_dto.model_dump_json(indent=2)}")

    # 4. Criar um AtualizarServicoDTO
    atualizar_servico_dto = AtualizarServicoDTO(
        descricao="Limpeza, verificação e recarga de gás para sistemas de ar condicionado.",
        valor_base=200.00
    )
    print(f"AtualizarServicoDTO (criado diretamente): {atualizar_servico_dto.model_dump_json(indent=2)}")

    # 5. Exemplo de como usar os dados do DTO
    print(f"Título do CriarServicoDTO: {criar_servico_dto.titulo}")
    print(f"Novo Valor Base do AtualizarServicoDTO: {atualizar_servico_dto.valor_base}")



# Exemplo de uso para Avaliacao
def exemplo_avaliacao_dto_pydantic():
    print("\n--- Exemplo de Avaliacao e AvaliacaoDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo Avaliacao (dataclass original)
    avaliacao_model = Avaliacao(
        id_avaliacao=1,
        id_avaliador=1,
        id_avaliado=101,
        nota=4.5,
        data_avaliacao=datetime(2024, 9, 15, 10, 30, 0),
        descricao="Ótimo serviço, muito profissional e atencioso.",
        nome_avaliador="João Silva",
        nome_avaliado="Serviços Rápidos Ltda."
    )
    print(f"Modelo Avaliacao (dataclass): {avaliacao_model}")

    # 2. Converter o modelo Avaliacao para AvaliacaoDTO (Pydantic)
    avaliacao_dto = CriarAvaliacaoDTO.model_validate(avaliacao_model)
    print(f"AvaliacaoDTO (convertido do modelo): {avaliacao_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarAvaliacaoDTO diretamente
    criar_avaliacao_dto = CriarAvaliacaoDTO(
        id_avaliador=2,
        id_avaliado=102,
        nota=5.0,
        descricao="Excelente! Superou as expectativas. Recomendo fortemente."
    )
    print(f"CriarAvaliacaoDTO (criado diretamente): {criar_avaliacao_dto.model_dump_json(indent=2)}")

    # 4. Criar um AtualizarAvaliacaoDTO
    atualizar_avaliacao_dto = AtualizarAvaliacaoDTO(
        nota=4.0,
        descricao="Bom serviço, mas o prazo foi um pouco estendido."
    )
    print(f"AtualizarAvaliacaoDTO (criado diretamente): {atualizar_avaliacao_dto.model_dump_json(indent=2)}")

    # 5. Exemplo de como usar os dados do DTO
    print(f"Nota do CriarAvaliacaoDTO: {criar_avaliacao_dto.nota}")
    print(f"Descrição do AtualizarAvaliacaoDTO: {atualizar_avaliacao_dto.descricao}")


# Exemplo de uso para Mensagem
def exemplo_mensagem_dto_pydantic():
    print("\n--- Exemplo de Mensagem e MensagemDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo Mensagem (dataclass original)
    mensagem_model = Mensagem(
        id_mensagem=1,
        id_remetente=1,
        id_destinatario=101,
        conteudo="Olá, gostaria de saber mais sobre o serviço de limpeza.",
        data_hora=datetime(2024, 9, 15, 11, 0, 0),
        nome_remetente="João Silva",
        nome_destinatario="Serviços Rápidos Ltda."
    )
    print(f"Modelo Mensagem (dataclass): {mensagem_model}")

    # 2. Converter o modelo Mensagem para MensagemDTO (Pydantic)
    mensagem_dto = CriarMensagemDTO.model_validate(mensagem_model)
    print(f"MensagemDTO (convertido do modelo): {mensagem_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarMensagemDTO diretamente
    criar_mensagem_dto = CriarMensagemDTO(
        id_remetente=101,
        id_destinatario=1,
        conteudo="Claro! Em que posso ajudar?"
    )
    print(f"CriarMensagemDTO (criado diretamente): {criar_mensagem_dto.model_dump_json(indent=2)}")

    # 4. Exemplo de como usar os dados do DTO
    print(f"Conteúdo do CriarMensagemDTO: {criar_mensagem_dto.conteudo}")


# Exemplo de uso para OrcamentoServico
def exemplo_orcamento_servico_dto_pydantic():
    print("\n--- Exemplo de OrcamentoServico e OrcamentoServicoDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo OrcamentoServico (dataclass original)
    orcamento_servico_model = OrcamentoServico(
        id_orcamento=1,
        id_servico=10,
        id_prestador=101,
        id_cliente=1,
        valor_estimado=250.00,
        data_solicitacao=date(2024, 10, 5),
        prazo_entrega=date(2024, 10, 20),
        status="pendente",
        descricao="Orçamento para instalação de ar condicionado.",
        nome_prestador="Climatiza Mais",
        nome_cliente="João Silva",
        titulo_servico="Instalação de AC"
    )
    print(f"Modelo OrcamentoServico (dataclass): {orcamento_servico_model}")

    # 2. Converter o modelo OrcamentoServico para OrcamentoServicoDTO (Pydantic)
    orcamento_servico_dto = CriarOrcamentoServicoDTO.model_validate(orcamento_servico_model)
    print(f"OrcamentoServicoDTO (convertido do modelo): {orcamento_servico_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarOrcamentoServicoDTO diretamente
    criar_orcamento_servico_dto = CriarOrcamentoServicoDTO(
        id_orcamento=2,
        id_servico=11,
        id_prestador=102,
        id_cliente=2,
        valor_estimado=150.00,
        prazo_entrega=date(2024, 10, 8),
        status="pendente",
        descricao="Orçamento para manutenção de jardim."
    )
    print(f"CriarOrcamentoServicoDTO (criado diretamente): {criar_orcamento_servico_dto.model_dump_json(indent=2)}")

    # 4. Criar um AtualizarOrcamentoServicoDTO
    atualizar_orcamento_servico_dto = AtualizarOrcamentoServicoDTO(
        status="aprovado",
        valor_estimado=140.00
    )
    print(f"AtualizarOrcamentoServicoDTO (criado diretamente): {atualizar_orcamento_servico_dto.model_dump_json(indent=2)}")

    # 5. Exemplo de como usar os dados do DTO
    print(f"Status do CriarOrcamentoServicoDTO: {criar_orcamento_servico_dto.status}")
    print(f"Novo Valor Estimado do AtualizarOrcamentoServicoDTO: {atualizar_orcamento_servico_dto.valor_estimado}")


# Exemplo de uso para Notificacao
def exemplo_notificacao_dto_pydantic():
    print("\n--- Exemplo de Notificacao e NotificacaoDTO (Pydantic) ---")

    # 1. Criar uma instância do modelo Notificacao (dataclass original)
    notificacao_model = Notificacao(
        id_notificacao=1,
        id_usuario=1,
        mensagem="Seu orçamento foi aprovado!",
        data_hora=datetime(2024, 10, 2, 14, 30, 0),
        tipo_notificacao="alerta",
        visualizar=False
    )
    print(f"Modelo Notificacao (dataclass): {notificacao_model}")

    # 2. Converter o modelo Notificacao para NotificacaoDTO (Pydantic)
    notificacao_dto = CriarNotificacaoDTO.model_validate(notificacao_model)
    print(f"NotificacaoDTO (convertido do modelo): {notificacao_dto.model_dump_json(indent=2)}")

    # 3. Criar um CriarNotificacaoDTO diretamente
    criar_notificacao_dto = CriarNotificacaoDTO(
        id_usuario=2,
        mensagem="Novo serviço disponível na sua área.",
        tipo_notificacao="informativo"
    )
    print(f"CriarNotificacaoDTO (criado diretamente): {criar_notificacao_dto.model_dump_json(indent=2)}")

    # 4. Criar um AtualizarNotificacaoDTO
    atualizar_notificacao_dto = AtualizarNotificacaoDTO(
        visualizar=True
    )
    print(f"AtualizarNotificacaoDTO (criado diretamente): {atualizar_notificacao_dto.model_dump_json(indent=2)}")

    # 5. Exemplo de como usar os dados do DTO
    print(f"Mensagem do CriarNotificacaoDTO: {criar_notificacao_dto.mensagem}")
    print(f"Status de visualização do AtualizarNotificacaoDTO: {atualizar_notificacao_dto.visualizar}")


# Exemplo de Validação com Falha
def exemplo_validacao_falha():
    print("\n--- Exemplo de Validação com Falha (Pydantic) ---")

    # Tentativa de criar um cliente com dados inválidos
    try:
        CriarClienteDTO(
            nome="A",  # Nome muito curto
            email="email_invalido",  # Email inválido
            senha="123",  # Senha muito curta
            cpf_cnpj="123",  # CPF/CNPJ inválido
            telefone="123",  # Telefone inválido
            cep="123",  # CEP inválido
            rua="R",  # Rua muito curta
            numero="12345678901",  # Número muito longo
            bairro="B",  # Bairro muito curto
            cidade="C",  # Cidade muito curta
            estado="XYZ",  # Estado inválido
        )
    except ValidationError as e:
        print("\nErro de validação ao criar cliente:")
        print(e)

    # Tentativa de criar um serviço com dados inválidos
    try:
        CriarServicoDTO(
            id_prestador=1,
            titulo="S",  # Título muito curto
            descricao="D",  # Descrição muito curta
            categoria="C",  # Categoria muito curta
            valor_base=-10,  # Valor negativo
        )
    except ValidationError as e:
        print("\nErro de validação ao criar serviço:")
        print(e)


if __name__ == "__main__":
    exemplo_cliente_dto_pydantic()
    exemplo_prestador_dto_pydantic()
    exemplo_servico_dto_pydantic()
    exemplo_avaliacao_dto_pydantic()
    exemplo_mensagem_dto_pydantic()
    exemplo_orcamento_servico_dto_pydantic()
    exemplo_notificacao_dto_pydantic()
    exemplo_validacao_falha()

