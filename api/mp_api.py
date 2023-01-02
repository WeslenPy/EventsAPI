from mercadopago import SDK
import app

class MercadoPago:
    def __init__(self,token,webhooks) -> SDK:
        self.api = SDK(token)
        self.webhook_url = webhooks


    def get_payment_preference(self, id_preference):
        preference_response = self.api.preference().get(id_preference)
        return preference_response["response"]


    def create_preference(self, id_pedido, valor, titulo_produto="Compra de ingresso - ModernPass",quantity=1):
        
        preference_data = {
            "notification_url":self.webhook_url['notify'],
            "back_urls": {
                "failure": self.webhook_url['failure'],
                "pending": self.webhook_url['pending'],
                "success": self.webhook_url['success']
            },
            "items": [
                {
                    "id": id_pedido,
                    "title": titulo_produto,
                    "quantity": quantity,
                    "currency_id": "BRL",
                    "unit_price": valor,
                }
            ]
        }

        preference_response = self.api.preference().create(preference_data)
        return preference_response["response"]

   
    def get_payment_info(self, id_ordem):
        """ Obtém as informações do pagamento """
        payment_info = self.api.payment().get(id_ordem)
        if payment_info["status"] == 200:
            return payment_info["response"]

