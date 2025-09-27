from utils.mercadopago_config import mp_config

class MercadoPagoService:
    def __init__(self):
        self.sdk = mp_config

    async def create_payment(self, payment_data: dict):
        try:
            payment_response = self.sdk.payment().create(payment_data)
            return payment_response
        except Exception as e:
            print(f"Erro ao criar pagamento no Mercado Pago: {e}")
            return None

    async def get_payment_status(self, payment_id: str):
        try:
            payment_status = self.sdk.payment().get(payment_id)
            return payment_status
        except Exception as e:
            print(f"Erro ao obter status do pagamento no Mercado Pago: {e}")
            return None
