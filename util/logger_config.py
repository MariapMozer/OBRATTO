"""
Configuração centralizada de logging para OBRATTO.

Cria logs em arquivo rotativo e console com níveis configuráveis.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import os

# Importar configuração
try:
    from util.config import LOG_LEVEL
except ImportError:
    # Fallback se config ainda não existir
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Criar diretório de logs se não existir
Path("logs").mkdir(exist_ok=True)

# Criar logger principal
logger = logging.getLogger("obratto")
logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

# Evitar duplicação de handlers
if not logger.handlers:
    # Handler para arquivo com rotação (10MB, 10 arquivos)
    file_handler = RotatingFileHandler(
        "logs/obratto.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Handler para console (mais conciso)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '[%(levelname)s] %(name)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

# Exportar logger configurado
__all__ = ['logger']
