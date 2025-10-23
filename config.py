from pathlib import Path
from util.template_util import criar_templates

# 1. Encontra o caminho absoluto para o diretório ONDE ESTE ARQUIVO (config.py) ESTÁ.
#    Ex: C:/Users/20221imi005/Desktop/obratto/OBRATTO/
# BASE_DIR = Path(__file__).resolve().parent

# 2. Define o caminho para a pasta de templates de forma absoluta.
#    Junta o caminho base com o nome da pasta "templates".
#    Ex: C:/Users/20221imi005/Desktop/obratto/OBRATTO/templates
# TEMPLATE_DIR = BASE_DIR / "templates"

# 3. Cria a instância de templates usando este caminho absoluto.
#    Agora não há como o programa se confundir sobre onde procurar.
#    Usa criar_templates() para registrar funções globais como get_flashed_messages
templates = criar_templates("templates")
