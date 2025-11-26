"""
Módulo de Configuração de Cache
Fornece estratégias de caching para otimização de performance
"""

from functools import wraps
from typing import Callable
from fastapi import Response
from datetime import datetime, timedelta


class CacheConfig:
    """
    Configuração de cache para diferentes tipos de recursos
    """

    # Durações de cache (em segundos)
    STATIC_ASSETS = 31536000  # 1 ano (assets versionados)
    CSS_JS = 86400  # 1 dia
    IMAGES = 604800  # 7 dias
    HTML = 0  # Sem cache (sempre validar)
    API_SHORT = 60  # 1 minuto
    API_MEDIUM = 300  # 5 minutos
    API_LONG = 3600  # 1 hora

    @staticmethod
    def get_cache_headers(max_age: int, must_revalidate: bool = False) -> dict:
        """
        Gera headers de cache HTTP

        Args:
            max_age: Tempo máximo de cache em segundos
            must_revalidate: Se True, força revalidação após expirar

        Returns:
            Dict com headers de cache
        """
        if max_age == 0:
            return {
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }

        directives = [f"max-age={max_age}", "public"]
        if must_revalidate:
            directives.append("must-revalidate")

        expires = datetime.utcnow() + timedelta(seconds=max_age)
        expires_str = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return {
            "Cache-Control": ", ".join(directives),
            "Expires": expires_str,
            "X-Cache-Control": "enabled"
        }

    @staticmethod
    def get_etag_headers(content: str) -> dict:
        """
        Gera ETag para validação de cache

        Args:
            content: Conteúdo para gerar hash

        Returns:
            Dict com header ETag
        """
        import hashlib
        etag = hashlib.md5(content.encode()).hexdigest()
        return {
            "ETag": f'"{etag}"'
        }


def cache_response(max_age: int = None, resource_type: str = "html"):
    """
    Decorator para adicionar headers de cache às respostas

    Args:
        max_age: Tempo de cache em segundos (opcional)
        resource_type: Tipo de recurso ('html', 'css', 'js', 'image', 'api')

    Uso:
        @app.get("/api/data")
        @cache_response(resource_type='api', max_age=300)
        async def get_data():
            return {"data": "value"}
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Executar a função original
            result = await func(*args, **kwargs)

            # Determinar max_age baseado no tipo de recurso
            cache_duration = max_age
            if cache_duration is None:
                cache_map = {
                    'html': CacheConfig.HTML,
                    'css': CacheConfig.CSS_JS,
                    'js': CacheConfig.CSS_JS,
                    'image': CacheConfig.IMAGES,
                    'static': CacheConfig.STATIC_ASSETS,
                    'api_short': CacheConfig.API_SHORT,
                    'api_medium': CacheConfig.API_MEDIUM,
                    'api_long': CacheConfig.API_LONG
                }
                cache_duration = cache_map.get(resource_type, CacheConfig.HTML)

            # Adicionar headers de cache
            if isinstance(result, Response):
                headers = CacheConfig.get_cache_headers(cache_duration)
                for key, value in headers.items():
                    result.headers[key] = value

            return result

        return wrapper
    return decorator


def no_cache(func: Callable):
    """
    Decorator para desabilitar cache completamente

    Uso:
        @app.get("/admin/dashboard")
        @no_cache
        async def admin_dashboard():
            return templates.TemplateResponse("admin/dashboard.html")
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)

        if isinstance(result, Response):
            headers = CacheConfig.get_cache_headers(0)
            for key, value in headers.items():
                result.headers[key] = value

        return result

    return wrapper


class StaticVersioning:
    """
    Sistema de versionamento de arquivos estáticos
    Adiciona hash aos URLs para cache busting
    """

    _version_cache = {}

    @classmethod
    def get_static_url(cls, path: str, version: str = None) -> str:
        """
        Gera URL de arquivo estático com versão

        Args:
            path: Caminho do arquivo estático (ex: '/static/css/components.css')
            version: Versão manual (opcional, usa hash automático se omitido)

        Returns:
            URL com parâmetro de versão

        Exemplo:
            get_static_url('/static/css/components.css')
            # Retorna: '/static/css/components.css?v=abc123'
        """
        if version:
            return f"{path}?v={version}"

        # Usar hash do arquivo como versão
        if path not in cls._version_cache:
            try:
                import hashlib
                from pathlib import Path

                # Remover /static/ do início para encontrar o arquivo
                file_path = path.replace('/static/', '', 1)
                full_path = Path(__file__).parent.parent / 'static' / file_path

                if full_path.exists():
                    with open(full_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()[:8]
                        cls._version_cache[path] = file_hash
                else:
                    cls._version_cache[path] = '1'
            except Exception:
                cls._version_cache[path] = '1'

        return f"{path}?v={cls._version_cache[path]}"

    @classmethod
    def clear_cache(cls):
        """Limpa o cache de versões (útil em desenvolvimento)"""
        cls._version_cache.clear()


# Jinja2 Filter para uso em templates
def static_versioned(path: str) -> str:
    """
    Filtro Jinja2 para adicionar versão a arquivos estáticos

    Uso no template:
        <link rel="stylesheet" href="{{ '/static/css/components.css' | static_versioned }}">
    """
    return StaticVersioning.get_static_url(path)
