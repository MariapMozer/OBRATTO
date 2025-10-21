# Guia Rápido - Sistema de Exception Handlers

## 🚀 Como Usar

### 1. Inicie o Servidor

```bash
uvicorn main:app --reload
```

Você verá no log:
```
[INFO] obratto - SessionMiddleware configurado
[INFO] obratto - Exception handlers registrados
```

### 2. Teste os Handlers

#### Teste 404 (Página Não Encontrada)
```
http://localhost:8000/rota-que-nao-existe
```
**Resultado esperado:** Página 404 personalizada

#### Teste 401 (Não Autenticado)
```
http://localhost:8000/fornecedor
```
(Sem estar logado como fornecedor)

**Resultado esperado:** Redirecionamento para `/login?redirect=/fornecedor`

#### Teste 500 (Erro Interno)

Adicione esta rota temporária ao `main.py` (antes do `if __name__...`):

```python
# ROTA DE TESTE - REMOVER EM PRODUÇÃO
@app.get("/test-error")
async def test_error():
    raise Exception("Teste de erro genérico")

@app.get("/test-validation")
async def test_validation():
    # Força erro de validação
    raise RequestValidationError(errors=[
        {
            "loc": ("body", "email"),
            "msg": "Email inválido",
            "type": "value_error"
        }
    ])
```

Acesse:
- `http://localhost:8000/test-error` → Erro 500
- `http://localhost:8000/test-validation` → Erro 422

**IMPORTANTE:** Remova essas rotas antes de fazer deploy em produção!

### 3. Verifique os Logs

```bash
tail -f logs/obratto.log
```

Você verá logs detalhados de cada erro:
```
2025-10-20 14:30:15 - obratto - [WARNING] - http_exception_handler:42 - HTTPException 404: Not Found - Path: /teste - IP: 127.0.0.1
2025-10-20 14:31:22 - obratto - [ERROR] - generic_exception_handler:157 - Exceção não tratada: Exception: Teste de erro genérico - Path: /test-error - IP: 127.0.0.1
```

## 🎯 Quando os Handlers São Acionados

### Automaticamente

Os handlers são acionados **automaticamente** quando:

1. **Rota não existe** → 404
2. **Decorador `@autenticar` bloqueia acesso** → 401/403
3. **Validação Pydantic falha** → 422
4. **Qualquer exceção não tratada** → 500

### Manualmente (Raise)

Você pode lançar exceções HTTP manualmente:

```python
from fastapi import HTTPException, status

@router.get("/minha-rota")
async def minha_rota(request: Request):
    if not alguma_condicao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso não encontrado"
        )
```

## 📝 Customizando Mensagens

### Flash Messages com Redirect

```python
from utils.flash_messages import informar_erro, informar_sucesso
from fastapi.responses import RedirectResponse

@router.post("/salvar")
async def salvar(request: Request):
    try:
        # Sua lógica aqui
        informar_sucesso(request, "Salvo com sucesso!")
        return RedirectResponse("/dashboard", status_code=303)
    except Exception as e:
        informar_erro(request, f"Erro ao salvar: {str(e)}")
        return RedirectResponse("/formulario", status_code=303)
```

## 🔧 Alternando Modos

### Modo Development (Detalhes Completos)

**Arquivo:** `.env`
```env
RUNNING_MODE=Development
LOG_LEVEL=DEBUG
```

**Exibe:**
- Stack traces completos
- Detalhes da requisição (path, method, IP)
- Body da requisição
- Erros de validação detalhados

### Modo Production (Seguro)

**Arquivo:** `.env`
```env
RUNNING_MODE=Production
LOG_LEVEL=INFO
```

**Exibe:**
- Mensagens genéricas e amigáveis
- Sem stack traces
- Sem detalhes técnicos
- "Nossa equipe foi notificada"

**Importante:** Logs completos são SEMPRE salvos, independente do modo!

## 🎨 Customizando Templates

### Modificar Página 404

**Arquivo:** `templates/errors/404.html`

```html
{% block conteudo %}
<div class="container my-5">
    <div class="error-container">
        <h1 class="error-code">404</h1>
        <h2 class="error-heading">Sua mensagem aqui</h2>
        <!-- Seu conteúdo customizado -->
    </div>
</div>
{% endblock %}
```

### Modificar Página 500

**Arquivo:** `templates/errors/500.html`

Similar ao 404, mas com suporte a `{{ error_message }}` e `{{ error_details }}`

### Modificar Estilos

**Arquivo:** `static/css/error_pages.css`

```css
.error-code {
    font-size: 10rem; /* Aumentar tamanho */
    color: #ff0000;   /* Mudar cor */
}
```

## 🐛 Debug e Troubleshooting

### Erro não está sendo capturado?

1. Verifique se os handlers foram registrados:
   ```bash
   grep "Exception handlers registrados" logs/obratto.log
   ```

2. Verifique a ordem no `main.py`:
   ```python
   # DEVE vir ANTES dos include_router
   app.add_exception_handler(StarletteHTTPException, http_exception_handler)
   app.add_exception_handler(RequestValidationError, validation_exception_handler)
   app.add_exception_handler(Exception, generic_exception_handler)
   ```

### Template não encontrado?

```bash
# Verificar se existem
ls -la templates/errors/
```

### CSS não está aplicado?

Certifique-se de que o template inclui:
```html
{% block css %}
<style>
    /* Estilos inline */
</style>
{% endblock %}
```

Ou adicione ao template base:
```html
<link rel="stylesheet" href="/static/css/error_pages.css">
```

## 📊 Monitoramento

### Ver últimos erros

```bash
# Últimos 20 erros
grep ERROR logs/obratto.log | tail -20

# Erros de hoje
grep "$(date +%Y-%m-%d)" logs/obratto.log | grep ERROR

# Contar erros por tipo
grep ERROR logs/obratto.log | awk '{print $6}' | sort | uniq -c
```

### Dashboard de Erros (Futuro)

Considere integrar:
- [Sentry](https://sentry.io) - Monitoramento de erros
- [Rollbar](https://rollbar.com) - Tracking de erros
- [Grafana](https://grafana.com) - Dashboards de logs

## ✅ Checklist de Produção

Antes de fazer deploy:

- [ ] `RUNNING_MODE=Production` no `.env`
- [ ] Remover rotas de teste (`/test-error`, etc)
- [ ] Configurar HTTPS (`https_only=True` no SessionMiddleware)
- [ ] Configurar SECRET_KEY segura
- [ ] Configurar rotação de logs adequada
- [ ] Testar todas as páginas de erro
- [ ] Verificar permissões da pasta `logs/`

## 🆘 Suporte

Em caso de problemas:

1. Verifique os logs: `logs/obratto.log`
2. Execute o teste de validação: `python3 test_exception_handlers_simple.py`
3. Consulte a documentação completa: `docs/EXCEPTION_HANDLERS_IMPLEMENTACAO.md`

---

**Versão:** 1.0.0
**Última atualização:** 20/10/2025
