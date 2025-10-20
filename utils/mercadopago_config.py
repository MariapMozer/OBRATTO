"""
Configuração e utilitários para integração com Mercado Pago
"""
# import mercadopago  # Comentado para simulação
import os
from typing import Dict, Any, Optional

class MercadoPagoConfig:
    """Configuração do Mercado Pago"""
    
    def __init__(self):
        # Chaves do Mercado Pago (usar variáveis de ambiente em produção)
        self.ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', 'TEST-YOUR-ACCESS-TOKEN-HERE')
        self.PUBLIC_KEY = os.getenv('MP_PUBLIC_KEY', 'TEST-YOUR-PUBLIC-KEY-HERE')
        
        # URLs de callback
        self.SUCCESS_URL = "http://127.0.0.1:8000/fornecedor/planos/pagamento/sucesso"
        self.FAILURE_URL = "http://127.0.0.1:8000/fornecedor/planos/pagamento/falha"
        self.PENDING_URL = "http://127.0.0.1:8000/fornecedor/planos/pagamento/pendente"
        
        # Inicializa o SDK
        # self.sdk = mercadopago.SDK(self.ACCESS_TOKEN)  # Comentado para simulação
        self.sdk = None
    
    def create_preference(self, plano_id: int, plano_nome: str, valor: float, fornecedor_id: int = 1) -> Dict[str, Any]:
        """
        Cria uma preferência de pagamento no Mercado Pago
        """
        try:
            preference_data = {
                "items": [
                    {
                        "title": f"Assinatura Plano {plano_nome} - OBRATTO",
                        "description": f"Plano {plano_nome} para fornecedores OBRATTO",
                        "quantity": 1,
                        "currency_id": "BRL",
                        "unit_price": float(valor)
                    }
                ],
                "payer": {
                    "name": "Fornecedor OBRATTO",
                    "email": "fornecedor@obratto.com"
                },
                "back_urls": {
                    "success": self.SUCCESS_URL,
                    "failure": self.FAILURE_URL,
                    "pending": self.PENDING_URL
                },
                "auto_return": "approved",
                "external_reference": f"plano_{plano_id}_fornecedor_{fornecedor_id}",
                "notification_url": "http://127.0.0.1:8000/fornecedor/planos/webhook/mercadopago",
                "metadata": {
                    "plano_id": plano_id,
                    "fornecedor_id": fornecedor_id,
                    "tipo": "assinatura_plano"
                }
            }

            assert self.sdk is not None
            preference_response = self.sdk.preference().create(preference_data)
            
            if preference_response["status"] == 201:
                return {
                    "success": True,
                    "preference_id": preference_response["response"]["id"],
                    "init_point": preference_response["response"]["init_point"],
                    "sandbox_init_point": preference_response["response"]["sandbox_init_point"]
                }
            else:
                return {
                    "success": False,
                    "error": preference_response["response"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_payment_info(self, payment_id: str) -> Dict[str, Any]:
        """
        Obtém informações de um pagamento específico
        """
        try:
            assert self.sdk is not None
            payment_response = self.sdk.payment().get(payment_id)
            return payment_response["response"]
        except Exception as e:
            return {"error": str(e)}
    
    def process_webhook(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa webhook do Mercado Pago
        """
        try:
            if notification_data.get("type") == "payment":
                payment_id = notification_data.get("data", {}).get("id")
                if payment_id:
                    payment_info = self.get_payment_info(payment_id)
                    return {
                        "success": True,
                        "payment_info": payment_info
                    }
            
            return {"success": False, "error": "Tipo de notificação não suportado"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Instância global
mp_config = MercadoPagoConfig()
