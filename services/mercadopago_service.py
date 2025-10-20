from util.mercadopago_config import mp_config
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class MercadoPagoService:
    """
    Serviço para integração com Mercado Pago.

    NOTA IMPORTANTE: Este serviço usa tokenização do Mercado Pago para processar
    pagamentos de forma segura. Cartões de crédito NÃO são armazenados localmente.
    Todo o processamento de cartões é feito através do Mercado Pago.

    Para assinaturas recorrentes, o Mercado Pago gerencia os tokens dos cartões
    e processa cobranças automáticas.
    """

    def __init__(self):
        self.config = mp_config

    async def create_payment(self, payment_data: dict):
        """
        Cria um pagamento no Mercado Pago.

        Args:
            payment_data: Dados do pagamento incluindo token do cartão

        Returns:
            Response do Mercado Pago com detalhes do pagamento
        """
        try:
            assert self.config.sdk is not None
            payment_response = self.config.sdk.payment().create(payment_data)
            return payment_response
        except Exception as e:
            logger.error(f"Erro ao criar pagamento no Mercado Pago: {e}")
            return None

    async def get_payment_status(self, payment_id: str):
        """
        Obtém o status de um pagamento específico.

        Args:
            payment_id: ID do pagamento no Mercado Pago

        Returns:
            Detalhes do pagamento incluindo status
        """
        try:
            assert self.config.sdk is not None
            payment_status = self.config.sdk.payment().get(payment_id)
            return payment_status
        except Exception as e:
            logger.error(f"Erro ao obter status do pagamento no Mercado Pago: {e}")
            return None

    async def create_card_token(self, card_data: dict) -> Optional[Dict[str, Any]]:
        """
        Cria um token de cartão no Mercado Pago para processamento seguro.

        IMPORTANTE: Tokens de cartão devem ser criados no frontend usando MercadoPago.js
        para segurança PCI compliance. Este método é para referência.

        Args:
            card_data: {
                "cardNumber": "número do cartão",
                "cardholderName": "nome do titular",
                "cardExpirationMonth": "mm",
                "cardExpirationYear": "yyyy",
                "securityCode": "cvv",
                "identificationType": "CPF",
                "identificationNumber": "cpf do titular"
            }

        Returns:
            Token do cartão para usar em pagamentos
        """
        try:
            assert self.config.sdk is not None
            token_response = self.config.sdk.card_token().create(card_data)

            if token_response["status"] == 201:
                return {
                    "success": True,
                    "token": token_response["response"]["id"],
                    "first_six_digits": token_response["response"]["first_six_digits"],
                    "last_four_digits": token_response["response"]["last_four_digits"]
                }
            else:
                logger.error(f"Erro ao criar token de cartão: {token_response}")
                return {"success": False, "error": token_response.get("message")}

        except Exception as e:
            logger.error(f"Erro ao criar token de cartão no Mercado Pago: {e}")
            return {"success": False, "error": str(e)}

    async def create_customer(self, email: str, first_name: str, last_name: str,
                             identification_type: str = "CPF",
                             identification_number: str = "") -> Optional[Dict[str, Any]]:
        """
        Cria um customer (pagador) no Mercado Pago para assinaturas recorrentes.

        Args:
            email: Email do cliente
            first_name: Primeiro nome
            last_name: Sobrenome
            identification_type: Tipo de documento (CPF, CNPJ, etc)
            identification_number: Número do documento

        Returns:
            Customer ID e detalhes
        """
        try:
            assert self.config.sdk is not None
            customer_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "identification": {
                    "type": identification_type,
                    "number": identification_number
                }
            }

            customer_response = self.config.sdk.customer().create(customer_data)

            if customer_response["status"] == 201:
                return {
                    "success": True,
                    "customer_id": customer_response["response"]["id"],
                    "email": customer_response["response"]["email"]
                }
            else:
                logger.error(f"Erro ao criar customer: {customer_response}")
                return {"success": False, "error": customer_response.get("message")}

        except Exception as e:
            logger.error(f"Erro ao criar customer no Mercado Pago: {e}")
            return {"success": False, "error": str(e)}

    async def save_card_to_customer(self, customer_id: str, card_token: str) -> Optional[Dict[str, Any]]:
        """
        Salva um cartão tokenizado para um customer (usado em assinaturas recorrentes).
        O cartão fica armazenado no Mercado Pago, não no nosso sistema.

        Args:
            customer_id: ID do customer no Mercado Pago
            card_token: Token do cartão criado previamente

        Returns:
            Card ID no Mercado Pago
        """
        try:
            assert self.config.sdk is not None
            card_data = {"token": card_token}

            card_response = self.config.sdk.card().create(customer_id, card_data)

            if card_response["status"] == 201:
                return {
                    "success": True,
                    "card_id": card_response["response"]["id"],
                    "last_four_digits": card_response["response"]["last_four_digits"],
                    "payment_method": card_response["response"]["payment_method"]["id"]
                }
            else:
                logger.error(f"Erro ao salvar cartão: {card_response}")
                return {"success": False, "error": card_response.get("message")}

        except Exception as e:
            logger.error(f"Erro ao salvar cartão no Mercado Pago: {e}")
            return {"success": False, "error": str(e)}

    async def create_subscription(self, customer_id: str, card_id: str,
                                  plan_value: float, plan_name: str,
                                  external_reference: str) -> Optional[Dict[str, Any]]:
        """
        Cria uma assinatura recorrente no Mercado Pago.

        Args:
            customer_id: ID do customer no MP
            card_id: ID do cartão salvo no MP
            plan_value: Valor do plano
            plan_name: Nome do plano
            external_reference: Referência externa para identificação

        Returns:
            Subscription ID e detalhes
        """
        try:
            assert self.config.sdk is not None

            subscription_data = {
                "payer_id": customer_id,
                "card_id": card_id,
                "transaction_amount": float(plan_value),
                "description": f"Assinatura {plan_name}",
                "external_reference": external_reference,
                "reason": plan_name,
                "auto_recurring": {
                    "frequency": 1,
                    "frequency_type": "months",
                    "transaction_amount": float(plan_value),
                    "currency_id": "BRL"
                }
            }

            subscription_response = self.config.sdk.subscription().create(subscription_data)

            if subscription_response["status"] in [200, 201]:
                return {
                    "success": True,
                    "subscription_id": subscription_response["response"]["id"],
                    "status": subscription_response["response"]["status"]
                }
            else:
                logger.error(f"Erro ao criar assinatura: {subscription_response}")
                return {"success": False, "error": subscription_response.get("message")}

        except Exception as e:
            logger.error(f"Erro ao criar assinatura no Mercado Pago: {e}")
            return {"success": False, "error": str(e)}

    async def cancel_subscription(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """
        Cancela uma assinatura recorrente.

        Args:
            subscription_id: ID da assinatura no Mercado Pago

        Returns:
            Confirmação do cancelamento
        """
        try:
            assert self.config.sdk is not None

            cancel_response = self.config.sdk.subscription().update(
                subscription_id,
                {"status": "cancelled"}
            )

            if cancel_response["status"] == 200:
                return {
                    "success": True,
                    "subscription_id": subscription_id,
                    "status": "cancelled"
                }
            else:
                logger.error(f"Erro ao cancelar assinatura: {cancel_response}")
                return {"success": False, "error": cancel_response.get("message")}

        except Exception as e:
            logger.error(f"Erro ao cancelar assinatura no Mercado Pago: {e}")
            return {"success": False, "error": str(e)}

    async def get_subscription_status(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém o status de uma assinatura.

        Args:
            subscription_id: ID da assinatura no Mercado Pago

        Returns:
            Detalhes da assinatura
        """
        try:
            assert self.config.sdk is not None
            subscription_response = self.config.sdk.subscription().get(subscription_id)

            if subscription_response["status"] == 200:
                return {
                    "success": True,
                    "subscription": subscription_response["response"]
                }
            else:
                return {"success": False, "error": subscription_response.get("message")}

        except Exception as e:
            logger.error(f"Erro ao obter status da assinatura: {e}")
            return {"success": False, "error": str(e)}
