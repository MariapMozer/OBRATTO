from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cliente/{id}")
async def get_cliente(request: Request, id: int):
    return templates.TemplateResponse("cliente.html", {"request": request, "cliente": "cliente"})

router = APIRouter(prefix="/cliente", tags=["Cliente"])

# Rota para Home do Cliente 
@router.get("/home_cliente/")
async def home_cliente(request: Request):
    return templates.TemplateResponse("cliente/home.html", {
        "request": request,
        "id_cliente": "id_cliente_logado",
        "pagina_ativa": "home"
    })


# Rota para exibir o formulário de cadastro do cliente
@router.get("/cliente/cadastro")
async def exibir_cadastro_cliente(request: Request):
    return templates.TemplateResponse("cliente/cadastro.html", {"request": request})


