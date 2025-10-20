"""
Rota de teste para o sistema de toasts
Acesse: http://localhost:8000/teste-toast para testar

Para usar em produção, importe as funções no seu código:
from utils.flash_messages import informar_sucesso, informar_erro, informar_aviso, informar_info
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from utils.flash_messages import informar_sucesso, informar_erro, informar_aviso, informar_info

router = APIRouter()


@router.get("/teste-toast", response_class=HTMLResponse)
async def teste_toast_page(request: Request):
    """Página de teste do sistema de toasts"""
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teste do Sistema de Toasts - Obratto</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/toasts.css">
    <style>
        body {
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .test-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .btn-test {
            margin: 5px;
            min-width: 150px;
        }
        .code-example {
            background: #f8f9fa;
            border-left: 4px solid #0d6efd;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="test-card">
            <div class="text-center mb-4">
                <h1 class="display-4">
                    <i class="bi bi-bell-fill text-primary"></i>
                    Sistema de Toasts
                </h1>
                <p class="lead text-muted">Teste o sistema de notificações do Obratto</p>
            </div>

            <hr class="my-4">

            <h3 class="mb-3"><i class="bi bi-lightning-fill text-warning"></i> Testes via Backend</h3>
            <p>Clique nos botões abaixo para testar as mensagens via backend (PRG pattern):</p>
            <div class="text-center mb-4">
                <a href="/teste-toast/flash-sucesso" class="btn btn-success btn-test">
                    <i class="bi bi-check-circle"></i> Sucesso
                </a>
                <a href="/teste-toast/flash-erro" class="btn btn-danger btn-test">
                    <i class="bi bi-x-circle"></i> Erro
                </a>
                <a href="/teste-toast/flash-aviso" class="btn btn-warning btn-test">
                    <i class="bi bi-exclamation-triangle"></i> Aviso
                </a>
                <a href="/teste-toast/flash-info" class="btn btn-info btn-test">
                    <i class="bi bi-info-circle"></i> Info
                </a>
                <a href="/teste-toast/flash-todos" class="btn btn-dark btn-test">
                    <i class="bi bi-collection"></i> Todos
                </a>
            </div>

            <div class="code-example">
                <strong>Exemplo de uso no backend:</strong><br>
                <code>
from utils.flash_messages import informar_sucesso<br>
<br>
@app.post("/criar-produto")<br>
async def criar(request: Request):<br>
&nbsp;&nbsp;&nbsp;&nbsp;informar_sucesso(request, "Produto criado com sucesso!")<br>
&nbsp;&nbsp;&nbsp;&nbsp;return RedirectResponse("/produtos", status_code=303)
                </code>
            </div>

            <hr class="my-4">

            <h3 class="mb-3"><i class="bi bi-code-square text-primary"></i> Testes via JavaScript</h3>
            <p>Clique nos botões abaixo para testar as mensagens via JavaScript:</p>
            <div class="text-center mb-4">
                <button onclick="window.exibirToast('Operação realizada com sucesso!', 'success')"
                        class="btn btn-success btn-test">
                    <i class="bi bi-check-circle"></i> JS Sucesso
                </button>
                <button onclick="window.exibirToast('Erro ao processar sua solicitação', 'danger')"
                        class="btn btn-danger btn-test">
                    <i class="bi bi-x-circle"></i> JS Erro
                </button>
                <button onclick="window.exibirToast('Esta ação não pode ser desfeita!', 'warning')"
                        class="btn btn-warning btn-test">
                    <i class="bi bi-exclamation-triangle"></i> JS Aviso
                </button>
                <button onclick="window.exibirToast('Você tem 3 novas mensagens', 'info')"
                        class="btn btn-info btn-test">
                    <i class="bi bi-info-circle"></i> JS Info
                </button>
                <button onclick="testeLongo()" class="btn btn-secondary btn-test">
                    <i class="bi bi-clock"></i> 10 segundos
                </button>
            </div>

            <div class="code-example">
                <strong>Exemplo de uso no frontend:</strong><br>
                <code>
// Função global<br>
window.exibirToast('Mensagem aqui', 'success');<br>
<br>
// Ou usar funções de conveniência:<br>
window.showSuccess('Salvo!');<br>
window.showError('Erro!');<br>
window.showWarning('Cuidado!');<br>
window.showInfo('FYI');
                </code>
            </div>

            <hr class="my-4">

            <div class="alert alert-info">
                <h5><i class="bi bi-info-circle-fill"></i> Informações</h5>
                <ul class="mb-0">
                    <li><strong>Posição:</strong> Inferior direito (customizável no CSS)</li>
                    <li><strong>Auto-dismiss:</strong> 5 segundos (customizável)</li>
                    <li><strong>Ícones:</strong> Bootstrap Icons integrados</li>
                    <li><strong>Framework:</strong> Bootstrap 5 nativo (sem dependências extras)</li>
                    <li><strong>Backend:</strong> Flash messages via sessão FastAPI</li>
                </ul>
            </div>

            <div class="text-center mt-4">
                <a href="/" class="btn btn-outline-primary">
                    <i class="bi bi-house"></i> Voltar para Home
                </a>
            </div>
        </div>
    </div>

    <!-- Container para Toasts -->
    <div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-4 toast-offset"></div>

    <!-- Dados de mensagens flash (hidden) -->
    <script id="mensagens-data" type="application/json">
        {{ get_flashed_messages(request) | tojson }}
    </script>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/toasts.js"></script>

    <script>
        // Teste de toast longo
        function testeLongo() {
            window.exibirToast(
                'Esta mensagem ficará visível por 10 segundos!',
                'info',
                10000
            );
        }

        // Avisar no console
        console.log('%c🎉 Sistema de Toasts carregado!', 'color: #0d6efd; font-size: 16px; font-weight: bold;');
        console.log('Use window.exibirToast(mensagem, tipo, duracao) para testar');
    </script>
</body>
</html>
    """)


@router.get("/teste-toast/flash-sucesso")
async def flash_sucesso(request: Request):
    """Testa mensagem de sucesso"""
    informar_sucesso(request, "✓ Mensagem de sucesso testada com sucesso!")
    return RedirectResponse("/teste-toast", status_code=303)


@router.get("/teste-toast/flash-erro")
async def flash_erro(request: Request):
    """Testa mensagem de erro"""
    informar_erro(request, "✗ Mensagem de erro testada! Algo deu errado.")
    return RedirectResponse("/teste-toast", status_code=303)


@router.get("/teste-toast/flash-aviso")
async def flash_aviso(request: Request):
    """Testa mensagem de aviso"""
    informar_aviso(request, "⚠ Mensagem de aviso testada! Atenção necessária.")
    return RedirectResponse("/teste-toast", status_code=303)


@router.get("/teste-toast/flash-info")
async def flash_info(request: Request):
    """Testa mensagem informativa"""
    informar_info(request, "ℹ Mensagem informativa testada! Para sua informação.")
    return RedirectResponse("/teste-toast", status_code=303)


@router.get("/teste-toast/flash-todos")
async def flash_todos(request: Request):
    """Testa todas as mensagens de uma vez"""
    informar_sucesso(request, "✓ Operação concluída com sucesso!")
    informar_info(request, "ℹ 150 registros foram processados")
    informar_aviso(request, "⚠ Alguns itens precisam de revisão")
    informar_erro(request, "✗ 3 itens falharam na validação")
    return RedirectResponse("/teste-toast", status_code=303)
