"""
Módulo de configurações centralizadas da aplicação OBRATTO.
Todas as configurações devem vir do arquivo .env
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# === Configurações da Aplicação ===
APP_NAME = os.getenv("APP_NAME", "OBRATTO")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION")
RUNNING_MODE = os.getenv("RUNNING_MODE", "Production")
IS_DEVELOPMENT = RUNNING_MODE.lower() == "development"

# === Configurações do Banco de Dados ===
DATABASE_PATH = os.getenv("DATABASE_PATH", "obratto.db")

# === Configurações do Servidor ===
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "False").lower() == "true"

# === Configurações de Email (Resend.com) ===
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "noreply@obratto.com")
RESEND_FROM_NAME = os.getenv("RESEND_FROM_NAME", APP_NAME)

# === Configurações de Logging ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# === Configurações de Rate Limiting ===
RATE_LIMIT_LOGIN_MAX = int(os.getenv("RATE_LIMIT_LOGIN_MAX", "5"))
RATE_LIMIT_LOGIN_MINUTOS = int(os.getenv("RATE_LIMIT_LOGIN_MINUTOS", "5"))
RATE_LIMIT_CADASTRO_MAX = int(os.getenv("RATE_LIMIT_CADASTRO_MAX", "3"))
RATE_LIMIT_CADASTRO_MINUTOS = int(os.getenv("RATE_LIMIT_CADASTRO_MINUTOS", "10"))
RATE_LIMIT_ESQUECI_SENHA_MAX = int(os.getenv("RATE_LIMIT_ESQUECI_SENHA_MAX", "1"))
RATE_LIMIT_ESQUECI_SENHA_MINUTOS = int(os.getenv("RATE_LIMIT_ESQUECI_SENHA_MINUTOS", "1"))

# === Configurações de Segurança ===
SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", "3600"))  # 1 hora
TOKEN_EXPIRACAO_HORAS = int(os.getenv("TOKEN_EXPIRACAO_HORAS", "1"))

# === Mercado Pago ===
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")
MERCADOPAGO_PUBLIC_KEY = os.getenv("MERCADOPAGO_PUBLIC_KEY", "")

# === Versão da Aplicação ===
VERSION = "1.0.0"
