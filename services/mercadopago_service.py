"""
Serviço MOCK de Mercado Pago para ambiente acadêmico.

IMPORTANTE: Este é um MOCK (simulação) do serviço de pagamento.
Não realiza transações reais. Ideal para demonstrações e testes.

Para uso em produção, seria necessário:
- Conta Mercado Pago ativa
- Credenciais de API (Access Token)
- SDK do Mercado Pago instalado
- Certificados SSL/HTTPS
"""

from typing import Dict, Any, Optional
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)


class MercadoPagoService:
    """
    Mock do serviço Mercado Pago.
    Simula pagamentos sem integração real.
    """

    def __init__(self):
        logger.info("🎭 Mercado Pago Mock Service inicializado (SEM integração real)")

    async def create_payment(self, payment_data: dict):
        """
        MOCK: Simula criação de pagamento.

        Args:
            payment_data: Dados do pagamento incluindo token do cartão

        Returns:
            Simulação de resposta do Mercado Pago
        """
        logger.info(f"💳 MOCK: Simulando pagamento de R$ {payment_data.get('transaction_amount', 0)}")

        # Simula aprovação automática
        mock_payment_id = f"MOCK-{random.randint(10000, 99999)}"

        return {
            "status": 201,
            "response": {
                "id": mock_payment_id,
                "status": "approved",
                "status_detail": "accredited",
                "transaction_amount": payment_data.get("transaction_amount", 0),
                "description": payment_data.get("description", "Pagamento"),
                "date_created": datetime.now().isoformat(),
                "date_approved": datetime.now().isoformat(),
                "payment_method_id": "mock_card",
                "payment_type_id": "credit_card",
                "mock": True
            }
        }

    async def get_payment_status(self, payment_id: str):
        """
        MOCK: Simula consulta de status de pagamento.

        Args:
            payment_id: ID do pagamento (simulado)

        Returns:
            Status simulado como "approved"
        """
        logger.info(f"🔍 MOCK: Consultando status do pagamento {payment_id}")

        return {
            "status": 200,
            "response": {
                "id": payment_id,
                "status": "approved",
                "status_detail": "accredited",
                "mock": True
            }
        }

    async def create_card_token(self, card_data: dict) -> Optional[Dict[str, Any]]:
        """
        MOCK: Simula criação de token de cartão.

        Args:
            card_data: Dados do cartão (não são armazenados)

        Returns:
            Token simulado
        """
        logger.info("💳 MOCK: Simulando tokenização de cartão")

        return {
            "success": True,
            "token": f"MOCK-TOKEN-{random.randint(1000, 9999)}",
            "first_six_digits": "123456",
            "last_four_digits": "1234",
            "mock": True
        }

    async def create_customer(self, email: str, first_name: str, last_name: str,
                             identification_type: str = "CPF",
                             identification_number: str = "") -> Optional[Dict[str, Any]]:
        """
        MOCK: Simula criação de customer.

        Args:
            email: Email do cliente
            first_name: Primeiro nome
            last_name: Sobrenome
            identification_type: Tipo de documento
            identification_number: Número do documento

        Returns:
            Customer ID simulado
        """
        logger.info(f"👤 MOCK: Criando customer para {email}")

        return {
            "success": True,
            "customer_id": f"MOCK-CUSTOMER-{random.randint(1000, 9999)}",
            "email": email,
            "mock": True
        }

    async def save_card_to_customer(self, customer_id: str, card_token: str) -> Optional[Dict[str, Any]]:
        """
        MOCK: Simula salvamento de cartão para customer.

        Args:
            customer_id: ID do customer (simulado)
            card_token: Token do cartão (simulado)

        Returns:
            Card ID simulado
        """
        logger.info(f"💾 MOCK: Salvando cartão para customer {customer_id}")

        return {
            "success": True,
            "card_id": f"MOCK-CARD-{random.randint(1000, 9999)}",
            "last_four_digits": "1234",
            "payment_method": "mock_card",
            "mock": True
        }

    async def create_subscription(self, customer_id: str, card_id: str,
                                  plan_value: float, plan_name: str,
                                  external_reference: str) -> Optional[Dict[str, Any]]:
        """
        MOCK: Simula criação de assinatura recorrente.

        Args:
            customer_id: ID do customer
            card_id: ID do cartão
            plan_value: Valor do plano
            plan_name: Nome do plano
            external_reference: Referência externa

        Returns:
            Subscription ID simulado
        """
        logger.info(f"🔄 MOCK: Criando assinatura {plan_name} - R$ {plan_value}/mês")

        return {
            "success": True,
            "subscription_id": f"MOCK-SUB-{random.randint(1000, 9999)}",
            "status": "authorized",
            "mock": True
        }

    async def cancel_subscription(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """
        MOCK: Simula cancelamento de assinatura.

        Args:
            subscription_id: ID da assinatura (simulado)

        Returns:
            Confirmação simulada
        """
        logger.info(f"❌ MOCK: Cancelando assinatura {subscription_id}")

        return {
            "success": True,
            "subscription_id": subscription_id,
            "status": "cancelled",
            "mock": True
        }

    async def get_subscription_status(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """
        MOCK: Simula consulta de status de assinatura.

        Args:
            subscription_id: ID da assinatura (simulado)

        Returns:
            Status simulado
        """
        logger.info(f"🔍 MOCK: Consultando status da assinatura {subscription_id}")

        return {
            "success": True,
            "subscription": {
                "id": subscription_id,
                "status": "authorized",
                "mock": True
            }
        }


# Mensagem de inicialização
logger.info("""
╔═══════════════════════════════════════════════════════════════╗
║             MERCADO PAGO - MODO SIMULAÇÃO (MOCK)              ║
╠═══════════════════════════════════════════════════════════════╣
║ ⚠️  Este serviço está em modo MOCK (simulação)                ║
║                                                               ║
║ ✅ Todos os pagamentos são aprovados automaticamente          ║
║ ✅ Não há cobranças reais                                     ║
║ ✅ Ideal para demonstrações e ambiente acadêmico             ║
║                                                               ║
║ Para produção, substituir por integração real com:           ║
║ - Conta Mercado Pago ativa                                   ║
║ - Credenciais de API válidas                                 ║
║ - SDK instalado: pip install mercadopago                     ║
╚═══════════════════════════════════════════════════════════════╝
""")
