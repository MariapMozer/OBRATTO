from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_repo import PagamentoRepository
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.inscricaoplano.inscricao_plano_repo import InscricaoPlanoRepository
from data.plano.plano_repo import PlanoRepository
from data.cartao.cartao_repo import CartaoRepository
from services.mercadopago_service import MercadoPagoService
from datetime import datetime

class PaymentService:
    def __init__(self):
        self.pagamento_repo = PagamentoRepository()
        self.inscricao_plano_repo = InscricaoPlanoRepository()
        self.plano_repo = PlanoRepository()
        self.cartao_repo = CartaoRepository()
        self.mercadopago_service = MercadoPagoService()

    async def process_plan_payment(self, prestador_id: int, plano_id: int, valor: float, metodo_pagamento: str, cartao_salvo_id: int = None, new_card_data: dict = None):
        plano = self.plano_repo.obter_plano_por_id(plano_id)
        if not plano:
            return {"success": False, "message": "Plano não encontrado.", "status_code": 404}

        # Check for active subscription
        assinatura_ativa = self.inscricao_plano_repo.obter_assinatura_ativa_por_prestador(prestador_id)
        if assinatura_ativa:
            return {"success": False, "message": "Você já possui uma assinatura ativa.", "status_code": 400}

        # Handle card data
        if cartao_salvo_id:
            cartao_usado = self.cartao_repo.obter_cartao_por_id(cartao_salvo_id)
            if not cartao_usado or cartao_usado.id_prestador != prestador_id:
                return {"success": False, "message": "Cartão selecionado não é válido.", "status_code": 400}
            # Use tokenized card or reference from Mercado Pago
            # For now, simulate with saved card
            payment_method_id = f"saved_card_{cartao_usado.id_cartao}"
        elif new_card_data:
            # Here, you would tokenize the card with Mercado Pago and get a payment_method_id
            # For now, simulate saving the card if requested
            if new_card_data.get("salvar_cartao") == "true":
                try:
                    mes_vencimento, ano_vencimento = new_card_data["validade"].split("/")
                    self.cartao_repo.criar_cartao_from_form(
                        id_prestador=prestador_id,
                        numero_cartao=new_card_data["numero_cartao"].replace(" ", ""),
                        nome_titular=new_card_data["nome_cartao"],
                        mes_vencimento=mes_vencimento,
                        ano_vencimento=ano_vencimento,
                        apelido=f"Cartão •••• {new_card_data["numero_cartao"].replace(" ", "")[-4:]}",
                        principal=False
                    )
                except Exception as e:
                    print(f"Erro ao salvar cartão: {e}")
            # Simulate payment method ID from new card
            payment_method_id = "new_card_payment"
        else:
            return {"success": False, "message": "Método de pagamento inválido.", "status_code": 400}

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

        # Prepare payment data for Mercado Pago
        payment_data = {
            "transaction_amount": float(valor),
            "description": f"Assinatura do plano {plano.nome_plano}",
            "payment_method_id": "visa", # This should come from tokenization or saved card
            "payer": {
                "email": "test_user_123@test.com" # Replace with actual user email
            },
            "external_reference": reference
        }

        # Process payment with Mercado Pago
        mp_response = await self.mercadopago_service.create_payment(payment_data)

        if mp_response and mp_response["status"] == 201:
            mp_payment_id = mp_response["response"]["id"]
            mp_status = mp_response["response"]["status"]
            mp_preference_id = mp_response["response"]["id"] # Assuming payment id can be used as preference id for now
        else:
            # Handle Mercado Pago error or simulation
            mp_payment_id = f"{metodo_pagamento}_payment_{inscricao_id}_{int(datetime.now().timestamp())}"
            mp_status = "pending" # Default to pending if MP fails or for simulation
            mp_preference_id = f"{metodo_pagamento}_pref_{inscricao_id}_{int(datetime.now().timestamp())}"
            print(f"Mercado Pago response error: {mp_response}")

        pagamento = Pagamento(
            id_pagamento=0,
            plano_id=plano_id,
            prestador_id=prestador_id,
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
            return {"success": True, "message": "Pagamento processado com sucesso!", "status": mp_status, "status_code": 200}
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

    def add_card(self, prestador_id: int, numero_cartao: str, nome_titular: str, mes_vencimento: str, ano_vencimento: str, apelido: str, principal: bool):
        # In a real scenario, this would involve tokenizing the card with Mercado Pago
        # and storing the token, not the full card number.
        # For now, it uses the existing repo method.
        return self.cartao_repo.criar_cartao_from_form(
            id_prestador=prestador_id,
            numero_cartao=numero_cartao,
            nome_titular=nome_titular,
            mes_vencimento=mes_vencimento,
            ano_vencimento=ano_vencimento,
            apelido=apelido,
            principal=principal
        )

    def update_card(self, id_cartao: int, prestador_id: int, nome_titular: str, apelido: str, principal: bool):
        cartao = self.cartao_repo.obter_cartao_por_id(id_cartao)
        if not cartao or cartao.id_prestador != prestador_id:
            return False
        cartao.nome_titular = nome_titular.strip().upper()
        cartao.apelido = apelido.strip()
        cartao.principal = principal
        return self.cartao_repo.atualizar_cartao(cartao)

    def delete_card(self, id_cartao: int, prestador_id: int):
        cartao = self.cartao_repo.obter_cartao_por_id(id_cartao)
        if not cartao or cartao.id_prestador != prestador_id:
            return False
        return self.cartao_repo.remover_cartao(id_cartao)

    def set_main_card(self, id_cartao: int, prestador_id: int):
        cartao = self.cartao_repo.obter_cartao_por_id(id_cartao)
        if not cartao or cartao.id_prestador != prestador_id:
            return False
        self.cartao_repo.definir_todos_nao_principal(prestador_id)
        cartao.principal = True
        return self.cartao_repo.atualizar_cartao(cartao)
