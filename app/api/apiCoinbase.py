import requests,json

class Coinbase:
    def __init__(self):

        self.TOKEN_API = '6b6aaea1-67b5-464c-b654-0932e144e73e'

        self.BASE_URL = 'https://api.commerce.coinbase.com/'

        self.HEADERS = {
            "Content-Type": "application/json",
            "X-CC-Version": "2018-03-22",
            "X-CC-Api-Key": self.TOKEN_API
        }

    def create_order(self, value):
        data = {
            "name": "Número Virtual - Bot",
            "description": "Transaction Panel",
            "local_price": {
                "amount": str(float(value)),
                "currency": "BRL"
            },
            "pricing_type": "fixed_price",
            "redirect_url": "https://www.painel.numerosvirtuais.com/painel"}

        response = requests.post(
            f'{self.BASE_URL}charges/', headers=self.HEADERS, data=json.dumps(data))
        try:
            data = response.json()

            return data['data']['code'], data['data']['hosted_url']
        except:
            return False

    def resolved_charge(self, _id):
        response = requests.post(
            f'{self.BASE_URL}charges/{_id}/resolve', headers=self.HEADERS)
        if response.status_code == 200:
            return True
        return False

    def update_order(self, _id):

        response = requests.get(
            f'{self.BASE_URL}charges/{_id}', headers=self.HEADERS)

        data = response.json()
        if 'timeline' in data['data']:
            status = data['data']['timeline'][-1]
            if status['status'] in ['CONFIRMED', 'RESOLVED', 'COMPLETED']:
                return True

            elif status['status'] == 'PENDING':

                payment = status['payment']['value']
                currency = payment['currency']
                cambio = data['data']['local_exchange_rates'][f'{currency}-BRL']

                return status['time'], payment['amount'], currency, cambio

        return False

