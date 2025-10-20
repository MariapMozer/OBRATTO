"""
Serviço de envio de emails usando Resend.com

Configuração: Defina RESEND_API_KEY no arquivo .env
"""
import os
from typing import Optional
from utils.logger_config import logger

# Tentar importar resend (pode não estar instalado)
try:
    import resend
    RESEND_DISPONIVEL = True
except ImportError:
    RESEND_DISPONIVEL = False
    logger.warning("Biblioteca 'resend' não instalada. Funcionalidade de email desabilitada.")

# Importar configurações
try:
    from util.config import (
        RESEND_API_KEY,
        RESEND_FROM_EMAIL,
        RESEND_FROM_NAME,
        BASE_URL
    )
except ImportError:
    RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'noreply@obratto.com')
    RESEND_FROM_NAME = os.getenv('RESEND_FROM_NAME', 'OBRATTO')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')


class EmailService:
    """
    Serviço para envio de emails via Resend.com
    
    Uso:
        email_service = EmailService()
        email_service.enviar_recuperacao_senha("user@example.com", "João", "token123")
    """
    
    def __init__(self):
        self.api_key = RESEND_API_KEY
        self.from_email = RESEND_FROM_EMAIL
        self.from_name = RESEND_FROM_NAME
        self.base_url = BASE_URL
        self.habilitado = RESEND_DISPONIVEL and bool(self.api_key)
        
        if self.habilitado:
            resend.api_key = self.api_key
            logger.info("EmailService inicializado com Resend.com")
        else:
            if not RESEND_DISPONIVEL:
                logger.warning("EmailService desabilitado: biblioteca 'resend' não instalada")
            elif not self.api_key:
                logger.warning("EmailService desabilitado: RESEND_API_KEY não configurada")
    
    def enviar_email(
        self,
        para_email: str,
        para_nome: str,
        assunto: str,
        html: str,
        texto: Optional[str] = None
    ) -> bool:
        """
        Envia e-mail genérico via Resend.com
        
        Args:
            para_email: Email do destinatário
            para_nome: Nome do destinatário
            assunto: Assunto do email
            html: Conteúdo HTML do email
            texto: Conteúdo texto plano (opcional)
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.habilitado:
            logger.warning(
                f"Tentativa de envio de email para {para_email} mas serviço está desabilitado. "
                "Configure RESEND_API_KEY no .env e instale: pip install resend"
            )
            return False
        
        params = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [para_email],
            "subject": assunto,
            "html": html
        }
        
        if texto:
            params["text"] = texto
        
        try:
            email = resend.Emails.send(params)
            logger.info(f"Email '{assunto}' enviado para {para_email} - ID: {email.get('id', 'N/A')}")
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar email para {para_email}: {e}")
            return False
    
    def enviar_recuperacao_senha(
        self,
        para_email: str,
        para_nome: str,
        token: str
    ) -> bool:
        """
        Envia email de recuperação de senha
        
        Args:
            para_email: Email do usuário
            para_nome: Nome do usuário
            token: Token de recuperação
        
        Returns:
            True se enviado com sucesso
        """
        url_recuperacao = f"{self.base_url}/resetar-senha?token={token}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f4f4f4; padding: 20px; }}
                .button {{ 
                    display: inline-block; 
                    padding: 12px 24px; 
                    background: #4CAF50; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 4px; 
                    margin: 20px 0;
                }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Recuperação de Senha</h1>
                </div>
                <div class="content">
                    <p>Olá <strong>{para_nome}</strong>,</p>
                    <p>Você solicitou a recuperação de senha para sua conta no <strong>OBRATTO</strong>.</p>
                    <p>Clique no botão abaixo para redefinir sua senha:</p>
                    <div style="text-align: center;">
                        <a href="{url_recuperacao}" class="button">Redefinir Senha</a>
                    </div>
                    <p>Ou copie e cole este link no navegador:</p>
                    <p style="word-break: break-all; background: white; padding: 10px; border-left: 4px solid #4CAF50;">
                        {url_recuperacao}
                    </p>
                    <p><strong>⚠️ Este link expira em 1 hora.</strong></p>
                    <p>Se você não solicitou esta recuperação, ignore este e-mail e sua senha permanecerá inalterada.</p>
                </div>
                <div class="footer">
                    <p>Este é um email automático, não responda.</p>
                    <p>&copy; 2025 OBRATTO. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        texto = f"""
        Recuperação de Senha - OBRATTO
        
        Olá {para_nome},
        
        Você solicitou a recuperação de senha para sua conta.
        
        Acesse este link para redefinir sua senha:
        {url_recuperacao}
        
        Este link expira em 1 hora.
        
        Se você não solicitou esta recuperação, ignore este e-mail.
        
        Atenciosamente,
        Equipe OBRATTO
        """
        
        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Recuperação de Senha - OBRATTO",
            html=html,
            texto=texto
        )
    
    def enviar_boas_vindas(
        self,
        para_email: str,
        para_nome: str,
        perfil: str
    ) -> bool:
        """
        Envia email de boas-vindas após cadastro
        
        Args:
            para_email: Email do novo usuário
            para_nome: Nome do usuário
            perfil: Perfil do usuário (Cliente, Fornecedor, etc)
        
        Returns:
            True se enviado com sucesso
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f4f4f4; padding: 20px; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Bem-vindo(a) ao OBRATTO!</h1>
                </div>
                <div class="content">
                    <p>Olá <strong>{para_nome}</strong>,</p>
                    <p>Seu cadastro como <strong>{perfil}</strong> foi realizado com sucesso!</p>
                    <p>Agora você pode acessar o sistema com seu e-mail e senha.</p>
                    <p>Acesse: <a href="{self.base_url}/login">{self.base_url}/login</a></p>
                    <p>Aproveite todas as funcionalidades da plataforma!</p>
                </div>
                <div class="footer">
                    <p>Este é um email automático, não responda.</p>
                    <p>&copy; 2025 OBRATTO. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        texto = f"""
        Bem-vindo(a) ao OBRATTO!
        
        Olá {para_nome},
        
        Seu cadastro como {perfil} foi realizado com sucesso!
        
        Agora você pode acessar o sistema com seu e-mail e senha.
        Acesse: {self.base_url}/login
        
        Aproveite todas as funcionalidades da plataforma!
        
        Atenciosamente,
        Equipe OBRATTO
        """
        
        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Bem-vindo(a) ao OBRATTO!",
            html=html,
            texto=texto
        )


# Instância global do serviço de email
email_service = EmailService()

__all__ = ['email_service', 'EmailService']
