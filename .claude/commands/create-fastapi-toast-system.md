---
description: Implementa sistema completo de notificações toast com Bootstrap 5
---

# Criar Sistema de Notificações Toast para FastAPI

Analisa, remove (se necessário) e implementa um sistema completo e elegante de notificações toast usando Bootstrap 5, integrado com flash messages do backend FastAPI para feedback visual ao usuário.

## Contexto

Este comando cria um sistema de notificações toast que:
- Integra com flash messages do backend (sessão FastAPI)
- Usa Bootstrap 5 toasts (sem dependências extras)
- Suporta 4 tipos de mensagens: sucesso, erro, aviso, info
- Auto-dismiss configurável (padrão: 5 segundos)
- Ícones Bootstrap Icons
- Posicionamento flexível (padrão: inferior direito)
- Remoção automática do DOM
- API JavaScript para uso programático

## FASE 1: Análise do Projeto Alvo

### 1.1 Verificar Sistema Existente

Execute análise para identificar sistemas de notificação existentes:

```bash
# Buscar por sistemas de toast/notificação
rg -i "(toast|notification|alert|flash|message)" --type js
rg -i "(toast|notification|alert|flash)" --type py

# Buscar por bibliotecas de notificação
rg -i "(toastr|notiflix|sweetalert|notyf|izitoast)" --type js

# Verificar dependências no package.json ou requirements
cat package.json 2>/dev/null | grep -i "toast\|notification\|alert"
```

### 1.2 Documentar Sistema Atual

Crie arquivo temporário `toast_analysis.md` documentando:
- Biblioteca usada (Toastr, SweetAlert, custom, etc.)
- Arquivos envolvidos (JS, CSS, templates)
- Como mensagens são passadas do backend para frontend
- Posicionamento e estilo das notificações
- Dependências externas

### 1.3 Confirmar com Usuário

**IMPORTANTE:** Antes de prosseguir, confirme:
1. Se deve remover sistema existente
2. Posicionamento preferido (bottom-right, top-right, etc.)
3. Tempo de auto-dismiss (padrão: 5 segundos)
4. Se precisa de tipos adicionais de mensagem

## FASE 2: Remoção do Sistema Antigo (se aplicável)

### 2.1 Backup

```bash
git add -A
git commit -m "Backup antes de remover sistema de notificações antigo"
```

### 2.2 Remover Componentes

1. **Bibliotecas JavaScript de notificação:**
   ```bash
   # Remover do HTML/templates
   # Exemplos: toastr.js, sweetalert.js, notiflix.js, etc.
   ```

2. **CSS de notificação:**
   ```bash
   # Remover imports/links de CSS
   # Exemplos: toastr.css, sweetalert.css, etc.
   ```

3. **Código JavaScript customizado:**
   - Remover arquivos de notificação customizados
   - Remover funções de toast/alert

4. **Desinstalar dependências (se via npm):**
   ```bash
   npm uninstall toastr sweetalert2 notiflix
   ```

## FASE 3: Implementação do Novo Sistema

### 3.1 Verificar Dependências

**IMPORTANTE:** Este sistema requer:
- ✅ Bootstrap 5.3+ (CSS e JS Bundle)
- ✅ Bootstrap Icons (para ícones nas mensagens)
- ✅ Jinja2 (para templates)
- ✅ FastAPI SessionMiddleware

Se o projeto **NÃO** tiver Bootstrap 5, adicione aos templates base:

```html
<!-- Bootstrap 5 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">

<!-- Bootstrap 5 JS Bundle (inclui Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
```

### 3.2 Arquivo: util/flash_messages.py

**Se este arquivo NÃO existir**, crie-o:

```python
from fastapi import Request
from typing import Literal

TipoMensagem = Literal["sucesso", "erro", "aviso", "info"]

def adicionar_mensagem(
    request: Request,
    mensagem: str,
    tipo: TipoMensagem = "info"
):
    """Adiciona mensagem flash à sessão"""
    if "mensagens" not in request.session:
        request.session["mensagens"] = []

    request.session["mensagens"].append({
        "texto": mensagem,
        "tipo": tipo
    })

def informar_sucesso(request: Request, mensagem: str):
    """Adiciona mensagem de sucesso"""
    adicionar_mensagem(request, mensagem, "sucesso")

def informar_erro(request: Request, mensagem: str):
    """Adiciona mensagem de erro"""
    adicionar_mensagem(request, mensagem, "erro")

def informar_aviso(request: Request, mensagem: str):
    """Adiciona mensagem de aviso"""
    adicionar_mensagem(request, mensagem, "aviso")

def informar_info(request: Request, mensagem: str):
    """Adiciona mensagem de informação"""
    adicionar_mensagem(request, mensagem, "info")

def obter_mensagens(request: Request) -> list:
    """Obtém e limpa mensagens da sessão"""
    mensagens = request.session.pop("mensagens", [])
    return mensagens
```

**Se já existir**, verifique se tem as funções:
- `informar_sucesso(request, mensagem)`
- `informar_erro(request, mensagem)`
- `informar_aviso(request, mensagem)`
- `informar_info(request, mensagem)`
- `obter_mensagens(request)`

Se não tiver, adicione as funções faltantes.

### 3.3 Arquivo: util/template_util.py

**Garantir que `obter_mensagens` está injetado nos templates:**

Se o arquivo **NÃO existir**, crie-o:

```python
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
from util.flash_messages import obter_mensagens

def criar_templates(pasta: str):
    """Cria Jinja2Templates com funções globais customizadas"""
    env = Environment(loader=FileSystemLoader("templates"))

    # Adicionar função global para obter mensagens
    env.globals['obter_mensagens'] = obter_mensagens

    templates = Jinja2Templates(env=env)
    return templates
```

Se já existir, verifique se tem:

```python
from util.flash_messages import obter_mensagens

# ... dentro de criar_templates():
env.globals['obter_mensagens'] = obter_mensagens
```

**Adaptar rotas para usar `criar_templates()`:**

Em todos os arquivos de rotas que usam templates:

```python
# ANTES (remover):
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

# DEPOIS (usar):
from util.template_util import criar_templates
templates = criar_templates("templates")
# ou
templates = criar_templates("templates/subpasta")
```

### 3.4 Arquivo: static/js/toasts.js

Crie o arquivo completo:

```javascript
/**
 * Sistema de Toasts Bootstrap 5
 * Lê mensagens do JSON e exibe como toasts Bootstrap 5
 *
 * Uso no backend:
 *   from util.flash_messages import informar_sucesso, informar_erro
 *   informar_sucesso(request, "Operação realizada com sucesso!")
 *   informar_erro(request, "Erro ao processar dados")
 *
 * Uso no frontend (programático):
 *   window.exibirToast('Mensagem aqui', 'success')
 *   window.exibirToast('Atenção!', 'warning')
 */

document.addEventListener('DOMContentLoaded', function() {
    // Obter mensagens do script JSON
    const mensagensElement = document.getElementById('mensagens-data');

    if (!mensagensElement) {
        return;
    }

    try {
        const mensagens = JSON.parse(mensagensElement.textContent || '[]');

        // Mapeamento de tipos de mensagem para classes Bootstrap
        const tipoMap = {
            'sucesso': 'success',
            'erro': 'danger',
            'aviso': 'warning',
            'info': 'info'
        };

        // Exibir cada mensagem
        mensagens.forEach(msg => {
            const tipoBootstrap = tipoMap[msg.tipo] || 'info';
            mostrarToast(msg.texto, tipoBootstrap);
        });
    } catch (e) {
        console.error('Erro ao processar mensagens:', e);
    }
});

/**
 * Exibe um toast na tela
 * @param {string} mensagem - Texto da mensagem
 * @param {string} tipo - Tipo do toast (success, danger, warning, info)
 * @param {number} delay - Tempo em ms antes de auto-dismiss (padrão: 5000)
 */
function mostrarToast(mensagem, tipo = 'info', delay = 5000) {
    const container = document.getElementById('toast-container');

    if (!container) {
        console.error('Container de toasts não encontrado');
        return;
    }

    // Gerar ID único para o toast
    const id = 'toast-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);

    // Criar elemento do toast
    const toastElement = document.createElement('div');
    toastElement.className = `toast align-items-center text-bg-${tipo} border-0`;
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');
    toastElement.id = id;

    // Ícones para cada tipo
    const icones = {
        'success': '<i class="bi bi-check-circle-fill me-2"></i>',
        'danger': '<i class="bi bi-exclamation-circle-fill me-2"></i>',
        'warning': '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
        'info': '<i class="bi bi-info-circle-fill me-2"></i>'
    };

    const icone = icones[tipo] || '';

    toastElement.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${icone}${mensagem}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto"
                    data-bs-dismiss="toast" aria-label="Fechar"></button>
        </div>
    `;

    // Adicionar ao container
    container.appendChild(toastElement);

    // Inicializar e mostrar toast
    const bsToast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: delay
    });

    bsToast.show();

    // Remover elemento do DOM após ser escondido
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

/**
 * Função global para exibir toasts programaticamente
 *
 * Exemplos:
 *   window.exibirToast('Salvo com sucesso!', 'success')
 *   window.exibirToast('Erro ao carregar', 'danger')
 *   window.exibirToast('Atenção necessária', 'warning')
 *   window.exibirToast('Informação útil', 'info')
 *   window.exibirToast('Mensagem longa', 'info', 10000) // 10 segundos
 */
window.exibirToast = mostrarToast;
```

### 3.5 Arquivo: static/css/custom.css

Adicione ao CSS customizado (ou crie se não existir):

```css
/* Toast container offset */
.toast-offset {
    margin-bottom: 60px; /* Ajuste conforme necessário */
}

/* Customizações opcionais para toasts */
.toast {
    min-width: 250px;
    max-width: 350px;
}

.toast-body {
    font-size: 0.95rem;
}

/* Animação suave */
.toast.showing {
    opacity: 1;
}

.toast:not(.show) {
    opacity: 0;
}
```

### 3.6 Atualizar Template Base

**Encontre o template base** (geralmente `base.html`, `base_publica.html`, `base_privada.html`, `layout.html`).

**Adicione ANTES do fechamento de `</body>`:**

```html
<!-- Container para Toasts -->
<!--
    Posicionamento: Altere as classes conforme necessidade:
    - bottom-0 end-0 = inferior direito
    - top-0 end-0 = superior direito
    - bottom-0 start-0 = inferior esquerdo
    - top-0 start-0 = superior esquerdo
-->
<div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-4 toast-offset"></div>

<!-- Dados de mensagens (hidden) -->
<script id="mensagens-data" type="application/json">
    {{ obter_mensagens(request) | tojson }}
</script>

<!-- SCRIPTS (ordem importa!) -->

<!-- Bootstrap 5 JS Bundle (se não tiver) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>

<!-- Script de Toasts -->
<script src="/static/js/toasts.js"></script>

<!-- Outros scripts do projeto -->
{% block scripts %}{% endblock %}
```

**IMPORTANTE:**
- O script `toasts.js` deve vir **DEPOIS** do Bootstrap JS
- O script `toasts.js` deve vir **ANTES** do block scripts
- O elemento `#mensagens-data` deve existir mesmo se vazio

**Se tiver múltiplos templates base**, adicione em todos.

### 3.7 Garantir SessionMiddleware

No arquivo `main.py` (ou `app.py`), garanta que `SessionMiddleware` está configurado:

```python
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()

# SessionMiddleware OBRIGATÓRIO para flash messages
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-mude-em-producao")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
```

### 3.8 Montar Arquivos Estáticos

No `main.py`, garanta que arquivos estáticos estão montados:

```python
from fastapi.staticfiles import StaticFiles

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
```

## FASE 4: Uso do Sistema

### 4.1 No Backend (Python)

Em qualquer rota FastAPI:

```python
from fastapi import Request
from fastapi.responses import RedirectResponse
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso, informar_info

@app.post("/exemplo")
async def exemplo(request: Request):
    # Sucesso (verde)
    informar_sucesso(request, "Operação realizada com sucesso!")

    # Erro (vermelho)
    informar_erro(request, "Erro ao processar dados. Tente novamente.")

    # Aviso (amarelo)
    informar_aviso(request, "Atenção: Esta ação não pode ser desfeita!")

    # Info (azul)
    informar_info(request, "Dados carregados: 150 registros encontrados.")

    # IMPORTANTE: Use redirect após mensagens flash
    return RedirectResponse("/destino", status_code=303)
```

**Padrão PRG (Post-Redirect-Get):**

```python
@app.post("/criar")
async def criar(request: Request, nome: str = Form(...)):
    try:
        # Lógica de criação
        criar_item(nome)

        # Mensagem de sucesso
        informar_sucesso(request, f"Item '{nome}' criado com sucesso!")

        # Redirecionar (PRG pattern)
        return RedirectResponse("/lista", status_code=303)

    except Exception as e:
        # Mensagem de erro
        informar_erro(request, f"Erro ao criar item: {str(e)}")

        # Redirecionar de volta
        return RedirectResponse("/criar", status_code=303)
```

### 4.2 No Frontend (JavaScript)

Para exibir toasts programaticamente via JavaScript:

```javascript
// Sucesso
window.exibirToast('Upload concluído!', 'success');

// Erro
window.exibirToast('Conexão perdida', 'danger');

// Aviso
window.exibirToast('Sessão expira em 5 minutos', 'warning');

// Info
window.exibirToast('Nova versão disponível', 'info');

// Com tempo customizado (10 segundos)
window.exibirToast('Mensagem importante', 'warning', 10000);
```

**Exemplo em evento:**

```html
<button onclick="salvar()">Salvar</button>

<script>
function salvar() {
    // Simular salvamento
    setTimeout(() => {
        window.exibirToast('Dados salvos com sucesso!', 'success');
    }, 1000);
}
</script>
```

## FASE 5: Customização

### 5.1 Alterar Posicionamento

No template base, altere as classes do container:

```html
<!-- Inferior Direito (padrão) -->
<div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-4 toast-offset"></div>

<!-- Superior Direito -->
<div id="toast-container" class="toast-container position-fixed top-0 end-0 p-4"></div>

<!-- Inferior Esquerdo -->
<div id="toast-container" class="toast-container position-fixed bottom-0 start-0 p-4"></div>

<!-- Superior Esquerdo -->
<div id="toast-container" class="toast-container position-fixed top-0 start-0 p-4"></div>

<!-- Centro Superior -->
<div id="toast-container" class="toast-container position-fixed top-0 start-50 translate-middle-x p-4"></div>
```

### 5.2 Alterar Tempo de Auto-Dismiss

**Globalmente** (em `toasts.js`):

```javascript
// Linha ~82
const bsToast = new bootstrap.Toast(toastElement, {
    autohide: true,
    delay: 10000  // 10 segundos (padrão: 5000)
});
```

**Por toast individual** (programático):

```javascript
window.exibirToast('Mensagem longa', 'info', 15000); // 15 segundos
```

### 5.3 Desabilitar Auto-Dismiss

```javascript
const bsToast = new bootstrap.Toast(toastElement, {
    autohide: false  // Usuário precisa fechar manualmente
});
```

### 5.4 Adicionar Tipos Customizados

**1. No backend (`util/flash_messages.py`):**

```python
def informar_custom(request: Request, mensagem: str):
    adicionar_mensagem(request, mensagem, "custom")
```

**2. No frontend (`static/js/toasts.js`):**

```javascript
// Adicionar ao mapeamento (linha ~21)
const tipoMap = {
    'sucesso': 'success',
    'erro': 'danger',
    'aviso': 'warning',
    'info': 'info',
    'custom': 'dark'  // ou 'light', 'primary', 'secondary'
};

// Adicionar ícone (linha ~60)
const icones = {
    'success': '<i class="bi bi-check-circle-fill me-2"></i>',
    'danger': '<i class="bi bi-exclamation-circle-fill me-2"></i>',
    'warning': '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
    'info': '<i class="bi bi-info-circle-fill me-2"></i>',
    'dark': '<i class="bi bi-gear-fill me-2"></i>'  // Ícone custom
};
```

### 5.5 Estilização Customizada

No `static/css/custom.css`:

```css
/* Toast com sombra maior */
.toast {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.25) !important;
}

/* Toast maior */
.toast {
    min-width: 300px;
    max-width: 400px;
}

/* Fonte maior */
.toast-body {
    font-size: 1rem;
}

/* Animação customizada */
@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.toast.show {
    animation: slideIn 0.3s ease-out;
}
```

## FASE 6: Testes

### 6.1 Teste Backend

Crie rota de teste temporária:

```python
from fastapi import Request
from fastapi.responses import HTMLResponse
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso, informar_info

@app.get("/teste-toast")
async def teste_toast(request: Request):
    informar_sucesso(request, "✓ Mensagem de sucesso testada!")
    informar_erro(request, "✗ Mensagem de erro testada!")
    informar_aviso(request, "⚠ Mensagem de aviso testada!")
    informar_info(request, "ℹ Mensagem de info testada!")

    return HTMLResponse("""
    <html>
    <head>
        <title>Teste Toast</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Teste de Toasts</h1>
            <p>Você deve ver 4 toasts no canto inferior direito.</p>
            <button onclick="window.exibirToast('Toast JavaScript!', 'success')">
                Testar Toast JS
            </button>
        </div>

        <div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-4"></div>

        <script id="mensagens-data" type="application/json">
            {{ obter_mensagens(request) | tojson }}
        </script>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
        <script src="/static/js/toasts.js"></script>
    </body>
    </html>
    """)
```

Acesse: `http://localhost:8000/teste-toast`

### 6.2 Teste Frontend

Console do navegador:

```javascript
// Testar cada tipo
window.exibirToast('Sucesso!', 'success');
window.exibirToast('Erro!', 'danger');
window.exibirToast('Aviso!', 'warning');
window.exibirToast('Info!', 'info');

// Testar tempo custom
window.exibirToast('10 segundos', 'info', 10000);
```

### 6.3 Teste Integração

Em uma rota real com formulário:

```python
@app.post("/login")
async def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    if autenticar(email, senha):
        informar_sucesso(request, f"Bem-vindo, {email}!")
        return RedirectResponse("/dashboard", status_code=303)
    else:
        informar_erro(request, "E-mail ou senha inválidos")
        return RedirectResponse("/login", status_code=303)
```

### 6.4 Verificar Logs do Console

Abra DevTools (F12) → Console e verifique:
- ✅ Sem erros de JavaScript
- ✅ Bootstrap carregado
- ✅ `toasts.js` carregado
- ✅ `window.exibirToast` definido

## FASE 7: Troubleshooting

### Problema: Toasts não aparecem

**Checklist:**
1. Bootstrap 5 JS carregado? (verifique console)
2. Container `#toast-container` existe no HTML?
3. Script `toasts.js` carregado?
4. Mensagens no JSON? (inspecionar `#mensagens-data`)
5. SessionMiddleware configurado?

**Debug:**
```javascript
// Console do navegador
console.log(document.getElementById('toast-container')); // Deve retornar elemento
console.log(typeof window.exibirToast); // Deve ser 'function'
console.log(typeof bootstrap); // Deve ser 'object'
```

### Problema: Toasts aparecem mas sem estilo

**Causa:** Bootstrap CSS não carregado

**Solução:**
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
```

### Problema: Ícones não aparecem

**Causa:** Bootstrap Icons não carregado

**Solução:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
```

### Problema: Mensagens não persistem entre requests

**Causa:** Flash messages consomem (pop) as mensagens na primeira leitura

**Comportamento esperado:** Mensagens aparecem UMA vez e são removidas da sessão.

### Problema: `bootstrap is not defined`

**Causa:** Bootstrap JS não carregado ou carregado depois de `toasts.js`

**Solução:** Garanta ordem correta:
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
<script src="/static/js/toasts.js"></script>
```

### Problema: Toasts aparecem sobrepostos ao footer

**Solução:** Ajustar `.toast-offset` no CSS:
```css
.toast-offset {
    margin-bottom: 80px; /* Aumentar valor */
}
```

## Checklist Final

- [ ] `util/flash_messages.py` criado/atualizado
- [ ] `util/template_util.py` criado/atualizado
- [ ] `obter_mensagens` injetado globalmente
- [ ] Rotas usando `criar_templates()`
- [ ] `static/js/toasts.js` criado
- [ ] `static/css/custom.css` atualizado
- [ ] Container `#toast-container` no template base
- [ ] Script `#mensagens-data` no template base
- [ ] Bootstrap 5 CSS carregado
- [ ] Bootstrap 5 JS carregado
- [ ] Bootstrap Icons carregado
- [ ] `toasts.js` carregado após Bootstrap
- [ ] SessionMiddleware configurado
- [ ] Arquivos estáticos montados
- [ ] Teste backend funcionando
- [ ] Teste frontend funcionando
- [ ] Sem erros no console
- [ ] Posicionamento correto
- [ ] Auto-dismiss funcionando

## Exemplos Práticos

### Exemplo 1: CRUD Completo

```python
@app.post("/produtos/criar")
async def criar_produto(request: Request, nome: str = Form(...), preco: float = Form(...)):
    try:
        produto = criar(nome, preco)
        informar_sucesso(request, f"Produto '{nome}' criado com sucesso!")
        return RedirectResponse("/produtos", status_code=303)
    except ValueError as e:
        informar_erro(request, str(e))
        return RedirectResponse("/produtos/criar", status_code=303)

@app.post("/produtos/{id}/atualizar")
async def atualizar_produto(request: Request, id: int, nome: str = Form(...)):
    try:
        atualizar(id, nome)
        informar_sucesso(request, "Produto atualizado!")
        return RedirectResponse("/produtos", status_code=303)
    except Exception as e:
        informar_erro(request, "Erro ao atualizar produto")
        return RedirectResponse(f"/produtos/{id}/editar", status_code=303)

@app.post("/produtos/{id}/excluir")
async def excluir_produto(request: Request, id: int):
    try:
        excluir(id)
        informar_aviso(request, "Produto excluído permanentemente")
        return RedirectResponse("/produtos", status_code=303)
    except Exception:
        informar_erro(request, "Não foi possível excluir o produto")
        return RedirectResponse("/produtos", status_code=303)
```

### Exemplo 2: Upload de Arquivo

```python
@app.post("/upload")
async def upload(request: Request, arquivo: UploadFile = File(...)):
    try:
        # Validar arquivo
        if arquivo.size > 5_000_000:
            informar_erro(request, "Arquivo muito grande (máx: 5MB)")
            return RedirectResponse("/upload", status_code=303)

        # Processar
        salvar_arquivo(arquivo)
        informar_sucesso(request, f"Arquivo '{arquivo.filename}' enviado com sucesso!")
        return RedirectResponse("/arquivos", status_code=303)

    except Exception as e:
        informar_erro(request, "Erro ao fazer upload do arquivo")
        return RedirectResponse("/upload", status_code=303)
```

### Exemplo 3: Validação Múltipla

```python
@app.post("/configurar")
async def configurar(request: Request, email: str = Form(...), telefone: str = Form(...)):
    erros = []

    if not validar_email(email):
        erros.append("E-mail inválido")

    if not validar_telefone(telefone):
        erros.append("Telefone inválido")

    if erros:
        for erro in erros:
            informar_erro(request, erro)
        return RedirectResponse("/configurar", status_code=303)

    # Salvar
    salvar_config(email, telefone)
    informar_sucesso(request, "Configurações salvas!")
    return RedirectResponse("/configurar", status_code=303)
```

## Adaptações para Outros Frameworks CSS

### Tailwind CSS

```javascript
// Modificar HTML do toast em toasts.js (linha ~69)
toastElement.innerHTML = `
    <div class="flex items-center p-4 rounded-lg shadow-lg ${getColorClass(tipo)}">
        <span class="mr-2">${icone}</span>
        <span class="flex-1">${mensagem}</span>
        <button onclick="this.closest('.toast').remove()" class="ml-4 text-white">×</button>
    </div>
`;

function getColorClass(tipo) {
    const cores = {
        'success': 'bg-green-500 text-white',
        'danger': 'bg-red-500 text-white',
        'warning': 'bg-yellow-500 text-white',
        'info': 'bg-blue-500 text-white'
    };
    return cores[tipo] || cores.info;
}
```

### Bulma CSS

Similar ao Tailwind - adaptar classes conforme documentação do Bulma.

## Melhorias Futuras

1. **Som de notificação:** Adicionar áudio sutil
2. **Animações avançadas:** Usar bibliotecas como Animate.css
3. **Ações no toast:** Botões "Desfazer", "Ver mais"
4. **Persistência:** Salvar histórico de notificações
5. **Agrupamento:** Agrupar mensagens similares
6. **Progress bar:** Indicador visual de tempo restante
7. **Priorização:** Toasts urgentes com destaque
8. **Múltiplos containers:** Diferentes posições simultâneas

## Conclusão

Você agora tem um sistema completo de notificações toast integrado com FastAPI, usando Bootstrap 5, sem dependências extras, com API simples tanto no backend quanto no frontend.

**Principais vantagens:**
- ✅ Zero dependências extras (só Bootstrap 5)
- ✅ Integração nativa com FastAPI sessions
- ✅ API simples e intuitiva
- ✅ Altamente customizável
- ✅ Acessível (ARIA)
- ✅ Responsivo
- ✅ Auto-dismiss configurável
- ✅ Limpeza automática do DOM
