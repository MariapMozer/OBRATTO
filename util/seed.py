from data.administrador.administrador_repo import criar_tabela_administrador
from data.anuncio.anuncio_repo import criar_tabela_anuncio
from data.avaliacao.avaliacao_repo import criar_tabela_avaliacao
from data.cliente.cliente_repo import criar_tabela_cliente
from data.fornecedor.fornecedor_repo import criar_tabela_fornecedor
from data.inscricaoplano.inscricao_plano_repo import criar_tabela_inscricao_plano
from data.mensagem.mensagem_repo import criar_tabela_mensagem
from data.notificacao.notificacao_repo import criar_tabela_notificacao
from data.orcamentoservico.orcamento_servico_repo import criar_tabela_orcamento_servico
from data.plano.plano_repo import criar_tabela_plano
from data.prestador.prestador_repo import criar_tabela_prestador
from data.produto.produto_repo import criar_tabela_produto
from data.servico.servico_repo import criar_tabela_servico
from data.usuario.usuario_repo import criar_tabela_usuario
from data.orcamento.orcamento_repo import criar_tabela_orcamento
from util.db import open_connection

def criar_tabelas():
    criar_tabela_usuario()
    criar_tabela_administrador()
    criar_tabela_prestador()
    criar_tabela_fornecedor()
    criar_tabela_cliente()
    criar_tabela_plano()
    criar_tabela_produto()
    criar_tabela_servico()
    criar_tabela_inscricao_plano()
    criar_tabela_orcamento()
    criar_tabela_anuncio()
    criar_tabela_avaliacao()
    criar_tabela_mensagem()
    criar_tabela_notificacao()
    criar_tabela_orcamento()
    criar_tabela_orcamento_servico()
    
    # Garantir que o fornecedor de teste sempre exista
    garantir_fornecedor_teste()


def garantir_fornecedor_teste():
    """
    Garante que o fornecedor de teste (ID 7) sempre exista no banco.
    Isso previne erros 404 na página de perfil do fornecedor.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        
        # Verificar se usuario ID 7 existe
        cursor.execute("SELECT id FROM usuario WHERE id = 7")
        usuario_existe = cursor.fetchone() is not None
        
        # Se usuario existe, garantir que fornecedor também exista
        if usuario_existe:
            cursor.execute("""
                INSERT OR IGNORE INTO fornecedor (id, razao_social, selo_confianca)
                VALUES (7, 'Lorenzo Barbosa Alves', 0)
            """)
            conn.commit()

