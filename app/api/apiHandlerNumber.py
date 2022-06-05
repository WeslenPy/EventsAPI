import requests,json


class NumberAPI:
    def __init__(self, baseUrlAPI, token,operator='any'):
        self.baseURL = str(baseUrlAPI).strip()
        self.token = str(token).strip()
        self.operator = str(operator).lower()

        self.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}

    def buy_number(self, sigla_service, country_code):
        operator = 'any' if str(country_code) != '73' else self.operator

        response = requests.get(
            f"{self.baseURL}?api_key={self.token}&action=getNumber&service={sigla_service}&country={country_code}&operator={operator}",headers=self.headers)
        response = response.text

        if 'ACCESS_NUMBER:' in response:
            status, id_number, number = str(response).split(':')
            self.active_status(id_number)

            return {'status': status, 'id': id_number, 'number': number, 'error': False}

        return {'error': True, 'status': response}

    def get_sms(self, activation_id):

        response = requests.get(
            f"{self.baseURL}?api_key={self.token}&action=getStatus&id={activation_id}")
        response = response.text

        if 'STATUS_OK' in response:
            status = response.split(':')[0]
            sms = ':'.join(response.split(':')[1:])
            self.get_new_sms(activation_id=activation_id)

            return {'sms': sms, 'status_api': status, 'status': True}

        return {'status': False, 'status_api': response}

    def get_new_sms(self, activation_id):
        requests.get(
            f"{self.baseURL}?api_key={self.token}&action=setStatus&status=3&id={activation_id}")
        return True

    def get_stock(self, country, symbol_service):
        operator = 'any' if str(country) != '73' else self.operator
        try:
            baseUrl = self.baseURL
            if 'https://api.smshub.org' in baseUrl:
                baseUrl= self.baseURL.replace('https://api.smshub.org','https://smshub.org')

            response = requests.get(
                f"{baseUrl}?api_key={self.token}&action=getNumbersStatus&country={country}&operator={operator}")

            data = json.loads(response.text.replace('\n', ''))

            symbol_service = f'{symbol_service}_0'
            if symbol_service in data:
                return {'error': False, 'status': True, 'amount': int(data[symbol_service])}

            return {'error': False, 'status': True, 'amount': 0}

        except Exception as error:
            return {'error': True, 'status': False, 'error_all': error, 'amount': 0}

    def active_status(self, activation_id):
        requests.get(
            f"{self.baseURL}?api_key={self.token}&action=setStatus&status=1&id={activation_id}")
        return True

    def cancel_number(self, activation_id):
        response = requests.get(
            f"{self.baseURL}?api_key={self.token}&action=setStatus&status=8&id={activation_id}")
        response = response.text 
        if response == 'ACCESS_CANCEL':
            return {'error': False, 'status': response}

        return {'error': True, 'status': response}


    def get_status(self,activation_id):
        response = requests.get(
            f"{self.baseURL}?api_key={self.token}&action=getStatus&id={activation_id}")
        response = response.text

        if ':' in response:response = response.split(':')[0]
        return response

