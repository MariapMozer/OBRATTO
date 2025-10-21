# Sistema de Notificações Toast - Obratto

Sistema completo de notificações toast integrado com Bootstrap 5 e flash messages do FastAPI.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Uso no Backend](#uso-no-backend)
- [Uso no Frontend](#uso-no-frontend)
- [Customização](#customização)
- [Testes](#testes)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O sistema de toasts do Obratto oferece:

- ✅ **Zero dependências extras** - Usa apenas Bootstrap 5 nativo
- ✅ **Integração com backend** - Flash messages via sessão FastAPI
- ✅ **API JavaScript** - Uso programático no frontend
- ✅ **4 tipos de mensagens** - Sucesso, erro, aviso, info
- ✅ **Auto-dismiss configurável** - Padrão: 5 segundos
- ✅ **Ícones integrados** - Bootstrap Icons
- ✅ **Responsivo** - Funciona em todos os dispositivos
- ✅ **Acessível** - ARIA labels e suporte a teclado

## 🏗️ Arquitetura

### Arquivos do Sistema

```
OBRATTO/
├── utils/
│   ├── flash_messages.py          # Sistema de flash messages
│   └── template_util.py            # Injeção de funções nos templates
├── static/
│   ├── js/
│   │   └── toasts.js               # Sistema de toasts JavaScript
│   └── css/
│       └── toasts.css              # Estilos customizados
└── templates/
    ├── cliente/base.html           # Template base cliente
    ├── prestador/base.html         # Template base prestador
    └── publico/
        ├── base.html               # Template base público
        └── base2.html              # Template base público alternativo
```

### Fluxo de Funcionamento

```
Backend (FastAPI)
    ↓
Flash Message na Sessão
    ↓
Template Renderizado (JSON no HTML)
    ↓
JavaScript (toasts.js)
    ↓
Bootstrap Toast Component
    ↓
Exibição Visual
```

## 💻 Uso no Backend

### Importar Funções

```python
from utils.flash_messages import (
    informar_sucesso,
    informar_erro,
    informar_aviso,
    informar_info
)
```

### Exemplos Práticos

#### 1. CRUD - Criar

```python
@router.post("/produtos/criar")
async def criar_produto(
    request: Request,
    nome: str = Form(...),
    preco: float = Form(...)
):
    try:
        produto = criar(nome, preco)
        informar_sucesso(request, f"Produto '{nome}' criado com sucesso!")
        return RedirectResponse("/produtos", status_code=303)
    except ValueError as e:
        informar_erro(request, f"Erro: {str(e)}")
        return RedirectResponse("/produtos/criar", status_code=303)
```

#### 2. CRUD - Atualizar

```python
@router.post("/produtos/{id}/atualizar")
async def atualizar_produto(
    request: Request,
    id: int,
    nome: str = Form(...)
):
    try:
        atualizar(id, nome)
        informar_sucesso(request, "Produto atualizado com sucesso!")
        return RedirectResponse("/produtos", status_code=303)
    except Exception:
        informar_erro(request, "Erro ao atualizar produto")
        return RedirectResponse(f"/produtos/{id}/editar", status_code=303)
```

#### 3. CRUD - Excluir

```python
@router.post("/produtos/{id}/excluir")
async def excluir_produto(request: Request, id: int):
    try:
        excluir(id)
        informar_aviso(request, "Produto excluído permanentemente")
        return RedirectResponse("/produtos", status_code=303)
    except Exception:
        informar_erro(request, "Não foi possível excluir o produto")
        return RedirectResponse("/produtos", status_code=303)
```

#### 4. Upload de Arquivo

```python
@router.post("/upload")
async def upload(request: Request, arquivo: UploadFile = File(...)):
    try:
        # Validar tamanho
        if arquivo.size > 5_000_000:
            informar_erro(request, "Arquivo muito grande (máx: 5MB)")
            return RedirectResponse("/upload", status_code=303)

        # Processar
        salvar_arquivo(arquivo)
        informar_sucesso(request, f"Arquivo '{arquivo.filename}' enviado!")
        return RedirectResponse("/arquivos", status_code=303)

    except Exception:
        informar_erro(request, "Erro ao fazer upload")
        return RedirectResponse("/upload", status_code=303)
```

#### 5. Login

```python
@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    usuario = autenticar(email, senha)

    if usuario:
        request.session["usuario_id"] = usuario.id
        informar_sucesso(request, f"Bem-vindo, {usuario.nome}!")
        return RedirectResponse("/dashboard", status_code=303)
    else:
        informar_erro(request, "E-mail ou senha inválidos")
        return RedirectResponse("/login", status_code=303)
```

#### 6. Validação Múltipla

```python
@router.post("/configurar")
async def configurar(
    request: Request,
    email: str = Form(...),
    telefone: str = Form(...)
):
    erros = []

    if not validar_email(email):
        erros.append("E-mail inválido")

    if not validar_telefone(telefone):
        erros.append("Telefone inválido")

    if erros:
        for erro in erros:
            informar_erro(request, erro)
        return RedirectResponse("/configurar", status_code=303)

    # Salvar configurações
    salvar_config(email, telefone)
    informar_sucesso(request, "Configurações salvas!")
    return RedirectResponse("/configurar", status_code=303)
```

#### 7. Múltiplas Mensagens

```python
@router.post("/processar-lote")
async def processar_lote(request: Request):
    resultado = processar()

    informar_info(request, f"{resultado['processados']} itens processados")

    if resultado['sucessos']:
        informar_sucesso(request, f"{resultado['sucessos']} itens com sucesso")

    if resultado['avisos']:
        informar_aviso(request, f"{resultado['avisos']} itens precisam revisão")

    if resultado['erros']:
        informar_erro(request, f"{resultado['erros']} itens falharam")

    return RedirectResponse("/resultado", status_code=303)
```

### ⚠️ Padrão PRG (Post-Redirect-Get)

**IMPORTANTE:** Sempre use `RedirectResponse` após adicionar mensagens flash:

```python
# ✅ CORRETO
informar_sucesso(request, "Salvo!")
return RedirectResponse("/destino", status_code=303)

# ❌ ERRADO - mensagem não aparecerá
informar_sucesso(request, "Salvo!")
return templates.TemplateResponse("pagina.html", {"request": request})
```

## 🎨 Uso no Frontend

### API JavaScript

#### Função Principal

```javascript
window.exibirToast(mensagem, tipo, duracao)
```

**Parâmetros:**
- `mensagem` (string): Texto da notificação
- `tipo` (string): `'success'`, `'danger'`, `'warning'`, `'info'`, `'primary'`
- `duracao` (number, opcional): Tempo em ms (padrão: 5000)

#### Exemplos

```javascript
// Sucesso
window.exibirToast('Dados salvos com sucesso!', 'success');

// Erro
window.exibirToast('Erro ao carregar dados', 'danger');

// Aviso
window.exibirToast('Sessão expira em 5 minutos', 'warning');

// Info
window.exibirToast('Nova versão disponível', 'info');

// Tempo customizado (10 segundos)
window.exibirToast('Mensagem importante', 'warning', 10000);

// Toast permanente (não fecha automaticamente)
window.exibirToast('Mensagem crítica', 'danger', 0);
```

#### Funções de Conveniência

```javascript
// Sucesso (5 segundos)
window.showSuccess('Operação concluída!');

// Erro (7 segundos)
window.showError('Falha na operação');

// Aviso (6 segundos)
window.showWarning('Atenção necessária');

// Info (5 segundos)
window.showInfo('Para sua informação');
```

### Uso em Eventos

```html
<!-- Botão com toast -->
<button onclick="window.exibirToast('Clicado!', 'success')">
    Clique Aqui
</button>

<!-- Formulário AJAX com toast -->
<script>
async function enviarFormulario(event) {
    event.preventDefault();

    try {
        const response = await fetch('/api/salvar', {
            method: 'POST',
            body: new FormData(event.target)
        });

        if (response.ok) {
            window.showSuccess('Formulário enviado com sucesso!');
        } else {
            window.showError('Erro ao enviar formulário');
        }
    } catch (error) {
        window.showError('Erro de conexão');
    }
}
</script>
```

## 🎨 Customização

### Posicionamento

Edite os templates base para alterar a posição do container:

```html
<!-- Inferior Direito (padrão) -->
<div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-4"></div>

<!-- Superior Direito -->
<div id="toast-container" class="toast-container position-fixed top-0 end-0 p-4"></div>

<!-- Inferior Esquerdo -->
<div id="toast-container" class="toast-container position-fixed bottom-0 start-0 p-4"></div>

<!-- Superior Esquerdo -->
<div id="toast-container" class="toast-container position-fixed top-0 start-0 p-4"></div>

<!-- Centro Superior -->
<div id="toast-container" class="toast-container position-fixed top-0 start-50 translate-middle-x p-4"></div>
```

### Tempo de Auto-Dismiss

#### Globalmente (toasts.js)

```javascript
// Linha ~100 em static/js/toasts.js
const bsToast = new bootstrap.Toast(toastElement, {
    autohide: true,
    delay: 8000  // Alterar para 8 segundos
});
```

#### Por Tipo (toasts.js)

```javascript
// Linhas ~135-150
window.showSuccess = function(message, duration = 5000) {
    return mostrarToast(message, 'success', duration);
};

window.showError = function(message, duration = 10000) {  // Erros mais tempo
    return mostrarToast(message, 'danger', duration);
};
```

### Cores Customizadas

Edite `static/css/toasts.css`:

```css
/* Sucesso mais escuro */
.toast.text-bg-success {
    background-color: #146c43 !important;
}

/* Erro mais vibrante */
.toast.text-bg-danger {
    background-color: #e63946 !important;
}

/* Aviso com preto */
.toast.text-bg-warning {
    background-color: #ffc107 !important;
    color: #000 !important;
}
```

### Ícones Personalizados

Edite `static/js/toasts.js` (linha ~75):

```javascript
const icones = {
    'success': '<i class="bi bi-check-circle-fill me-2"></i>',
    'danger': '<i class="bi bi-x-octagon-fill me-2"></i>',      // Mudou
    'warning': '<i class="bi bi-exclamation-diamond-fill me-2"></i>', // Mudou
    'info': '<i class="bi bi-lightbulb-fill me-2"></i>',        // Mudou
    'primary': '<i class="bi bi-megaphone-fill me-2"></i>'      // Mudou
};
```

### Tamanho dos Toasts

Edite `static/css/toasts.css`:

```css
.toast {
    min-width: 300px;  /* Aumentar largura */
    max-width: 450px;
    font-size: 1rem;   /* Aumentar fonte */
}
```

## 🧪 Testes

### Página de Teste

Acesse: **http://localhost:8000/teste-toast**

Esta página permite testar:
- ✅ Mensagens via backend (PRG pattern)
- ✅ Mensagens via JavaScript
- ✅ Todos os tipos de mensagem
- ✅ Múltiplas mensagens simultâneas
- ✅ Tempo customizado

### Teste Manual via Console

Abra o Console do navegador (F12):

```javascript
// Testar cada tipo
window.exibirToast('Teste sucesso', 'success');
window.exibirToast('Teste erro', 'danger');
window.exibirToast('Teste aviso', 'warning');
window.exibirToast('Teste info', 'info');

// Verificar se sistema está funcionando
console.log(typeof window.exibirToast);  // Deve retornar 'function'
console.log(typeof bootstrap);            // Deve retornar 'object'
```

### Teste de Integração

Crie uma rota simples:

```python
@router.get("/teste-integracao")
async def teste(request: Request):
    informar_sucesso(request, "Sistema funcionando!")
    return RedirectResponse("/", status_code=303)
```

Acesse a rota e verifique se o toast aparece.

## 🔧 Troubleshooting

### Problema: Toasts não aparecem

**Checklist:**

1. ✅ Bootstrap 5 JS carregado?
   ```html
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
   ```

2. ✅ Container existe?
   ```html
   <div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-4"></div>
   ```

3. ✅ Script toasts.js carregado APÓS Bootstrap?
   ```html
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
   <script src="/static/js/toasts.js"></script>
   ```

4. ✅ Script de dados existe?
   ```html
   <script id="mensagens-data" type="application/json">
       {{ get_flashed_messages(request) | tojson }}
   </script>
   ```

5. ✅ SessionMiddleware configurado no main.py?
   ```python
   app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
   ```

### Problema: Toasts sem estilo

**Causa:** Bootstrap CSS não carregado

**Solução:**
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
```

### Problema: Ícones não aparecem

**Causa:** Bootstrap Icons não carregado

**Solução:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
```

### Problema: Erro "bootstrap is not defined"

**Causa:** Bootstrap JS não carregado ou ordem errada

**Solução:** Garanta a ordem correta:
```html
<!-- 1. Bootstrap primeiro -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
<!-- 2. Toasts depois -->
<script src="/static/js/toasts.js"></script>
```

### Problema: Mensagens não persistem entre requests

**Comportamento esperado:** Flash messages são consumidas (pop) na primeira leitura.

As mensagens devem aparecer UMA vez e serem removidas automaticamente da sessão.

### Debug no Console

```javascript
// Verificar container
console.log(document.getElementById('toast-container'));

// Verificar função
console.log(typeof window.exibirToast);

// Verificar Bootstrap
console.log(typeof bootstrap);

// Verificar mensagens no JSON
const dados = document.getElementById('mensagens-data');
console.log(JSON.parse(dados.textContent));
```

## 📚 Referências

- [Bootstrap 5 Toasts](https://getbootstrap.com/docs/5.3/components/toasts/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [FastAPI Sessions](https://www.starlette.io/middleware/#sessionmiddleware)
- [Flash Messages Pattern](https://en.wikipedia.org/wiki/Post/Redirect/Get)

## 🎓 Melhores Práticas

1. **Sempre use PRG pattern** com mensagens flash
2. **Seja específico** nas mensagens (evite "Erro" genérico)
3. **Use o tipo correto** (sucesso, erro, aviso, info)
4. **Não abuse** de múltiplas mensagens simultâneas
5. **Teste em mobile** para verificar responsividade
6. **Mantenha mensagens curtas** (máx 2 linhas)

## ✅ Checklist de Implementação

- [x] `utils/flash_messages.py` criado/atualizado
- [x] `utils/template_util.py` atualizado com injeção de funções
- [x] `static/js/toasts.js` criado
- [x] `static/css/toasts.css` criado
- [x] Templates base atualizados (cliente, prestador, publico)
- [x] Container `#toast-container` adicionado
- [x] Script `#mensagens-data` adicionado
- [x] Bootstrap 5 CSS/JS carregados
- [x] Bootstrap Icons carregado
- [x] SessionMiddleware configurado
- [x] Rota de teste criada

---

**Sistema implementado com sucesso! 🎉**

Para dúvidas ou sugestões, acesse: http://localhost:8000/teste-toast
