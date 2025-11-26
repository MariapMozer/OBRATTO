from fastapi import Request
from fastapi.templating import Jinja2Templates
from util.flash_messages import get_flashed_messages

# Template global context
templates = Jinja2Templates(directory="templates")

# Adicionar funções globais aos templates
templates.env.globals["get_flashed_messages"] = get_flashed_messages