from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_repo import PagamentoRepository
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.inscricaoplano import inscricao_plano_repo
from data.plano.plano_repo import PlanoRepository
from services.mercadopago_service import MercadoPagoService
from datetime import datetime
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Serviço de pagamento integrado com Mercado Pago.

    NOTA IMPORTANTE: Este serviço NÃO armazena dados de cartões de crédito localmente.
    Toda a gestão de cartões e tokenização é feita através do Mercado Pago.

    Para assinaturas recorrentes, o Mercado Pago gerencia os tokens dos cartões
    e processa cobranças automáticas.
    """

    def __init__(self):
        self.pagamento_repo = PagamentoRepository()
        self.inscricao_plano_repo = inscricao_plano_repo
        self.plano_repo = PlanoRepository()
        self.mercadopago_service = MercadoPagoService()

    async def process_plan_payment(self, prestador_id: int, plano_id: int, valor: float,
                                   metodo_pagamento: str, card_token: Optional[str] = None,
                                   user_email: Optional[str] = None):
        """
        Processa pagamento de plano usando token de cartão do Mercado Pago.

        IMPORTANTE: Este método NÃO salva dados de cartão localmente.
        O card_token deve ser gerado no frontend usando MercadoPago.js

        Args:
            prestador_id: ID do prestador/fornecedor
            plano_id: ID do plano sendo assinado
            valor: Valor do pagamento
            metodo_pagamento: Método de pagamento (ex: "credit_card")
            card_token: Token do cartão gerado pelo Mercado Pago
            user_email: Email do usuário para processamento

        Returns:
            Resultado do processamento do pagamento
        """
        plano = self.plano_repo.obter_plano_por_id(plano_id)
        if not plano:
            return {"success": False, "message": "Plano não encontrado.", "status_code": 404}

        # Check for active subscription
        assinatura_ativa = self.inscricao_plano_repo.obter_assinatura_ativa_por_prestador(prestador_id)
        if assinatura_ativa:
            return {"success": False, "message": "Você já possui uma assinatura ativa.", "status_code": 400}

        # Validate card token
        if not card_token:
            return {"success": False, "message": "Token de cartão não fornecido.", "status_code": 400}

        # Create new subscription entry
        nova_inscricao = InscricaoPlano(
            id_inscricao_plano=0,
            id_prestador=prestador_id,
            id_plano=plano_id
        )
        inscricao_id = self.inscricao_plano_repo.inserir_inscricao_plano(nova_inscricao)
        if not inscricao_id:
            return {"success": False, "message": "Erro ao criar inscrição do plano.", "status_code": 500}

        reference = f"assinatura_plano_{plano_id}_prestador_{prestador_id}_{inscricao_id}"

        # Prepare payment data for Mercado Pago using token
        payment_data = {
            "transaction_amount": float(valor),
            "token": card_token,  # Use token instead of raw card data
            "description": f"Assinatura do plano {plano.nome_plano}",
            "installments": 1,
            "payment_method_id": metodo_pagamento,
            "payer": {
                "email": user_email or "user@obratto.com"
            },
            "external_reference": reference
        }

        # Process payment with Mercado Pago
        mp_response = await self.mercadopago_service.create_payment(payment_data)

        if mp_response and mp_response["status"] == 201:
            mp_payment_id = mp_response["response"]["id"]
            mp_status = mp_response["response"]["status"]
            mp_preference_id = mp_response["response"]["id"]
        else:
            # Handle Mercado Pago error or simulation mode
            mp_payment_id = f"{metodo_pagamento}_payment_{inscricao_id}_{int(datetime.now().timestamp())}"
            mp_status = "pending"  # Default to pending if MP fails or for simulation
            mp_preference_id = f"{metodo_pagamento}_pref_{inscricao_id}_{int(datetime.now().timestamp())}"
            logger.error(f"Mercado Pago response error: {mp_response}")

        pagamento = Pagamento(
            id_pagamento=0,
            plano_id=plano_id,
            fornecedor_id=prestador_id,
            mp_payment_id=str(mp_payment_id),
            mp_preference_id=str(mp_preference_id),
            valor=valor,
            status=mp_status,
            metodo_pagamento=metodo_pagamento,
            data_criacao=datetime.now().isoformat(),
            data_aprovacao=datetime.now().isoformat() if mp_status == "approved" else None,
            external_reference=reference
        )

        pagamento_inserido = self.pagamento_repo.inserir_pagamento(pagamento)
        if pagamento_inserido:
            return {
                "success": True,
                "message": "Pagamento processado com sucesso!",
                "status": mp_status,
                "payment_id": mp_payment_id,
                "status_code": 200
            }
        else:
            return {"success": False, "message": "Erro ao registrar pagamento no banco de dados.", "status_code": 500}

    async def handle_mercadopago_webhook(self, notification_data: dict):
        # In a real scenario, you\"d validate the notification and fetch payment details from MP API
        # For this example, we\"ll assume notification_data contains enough info
        topic = notification_data.get("topic")
        resource_id = notification_data.get("id")

        if topic == "payment" and resource_id:
            mp_payment_details = await self.mercadopago_service.get_payment_status(resource_id)
            if mp_payment_details and mp_payment_details["status"] == 200:
                payment_info = mp_payment_details["response"]
                mp_payment_id = payment_info["id"]
                mp_status = payment_info["status"]
                external_reference = payment_info["external_reference"]

                # Find the payment in your DB using external_reference or mp_payment_id
                pagamento = self.pagamento_repo.obter_pagamento_por_mp_id(mp_payment_id)
                if pagamento:
                    pagamento.status = mp_status
                    if mp_status == "approved":
                        pagamento.data_aprovacao = datetime.now().isoformat()
                        # Activate plan here if not already active
                        # self.inscricao_plano_repo.ativar_plano(pagamento.inscricao_id)
                    self.pagamento_repo.atualizar_pagamento(pagamento)
                    return {"success": True, "message": f"Pagamento {mp_payment_id} atualizado para {mp_status}"}
                else:
                    return {"success": False, "message": f"Pagamento com MP ID {mp_payment_id} não encontrado no DB."}
        return {"success": False, "message": "Notificação de webhook inválida ou não processada."}