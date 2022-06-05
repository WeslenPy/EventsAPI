from datetime import datetime,timedelta
from uuid import uuid4
import requests,json

class Picpay:
    def __init__(self) -> None:

        self.API = 'https://appws.picpay.com/ecommerce/public/payments'

        self.TOKEN_PICPAY = 'b9796607-c08d-4c7f-9c4c-759cdbb35d5c'

        self.headers = {'x-picpay-token': self.TOKEN_PICPAY,
                        'Content-Type': 'application/json'}

    def create_order(self, value,cpf):

        expires = f"{(datetime.now()+timedelta(minutes=20)).strftime('%Y-%m-%dT%H:%M:%S')}-03:00"
        referenceId = str(uuid4())
        payment = {'referenceId': referenceId,
                   "callbackUrl": 'https://www.painel.numerosvirtuais.com/webhook/picpay/checkout',
                   "expiresAt": expires,
                   "returnUrl": "https://www.painel.numerosvirtuais.com/painel",
                   "value":f"{value:.2f}",
                   "buyer":{'document':str(cpf)}}

        response = requests.post(
            self.API, headers=self.headers, data=json.dumps(payment))

        if response.status_code == 200:
            return response.json()['paymentUrl'], referenceId

        return False

    def get_status(self, referenceId):

        response = requests.get(
            f'{self.API}/{referenceId}/status', headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return False

