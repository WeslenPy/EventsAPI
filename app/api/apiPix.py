from datetime import datetime,timedelta
import base64,requests,pyqrcode,json
from time import sleep


class Pix:
    def __init__(self):

        self.TIME = datetime.timestamp(datetime.now()+timedelta(minutes=6))

        self.CLIENT_ID = 'Client_Id_62e15265072d8560617f4752dcf5f324dca55f91'
        self.CLIENT_SECRET = 'Client_Secret_fa1085e3617f1b1c59d84470cefe7a9dfeaf33f2'
        self.CERTIFICATE = './certs/certificado.pem'
        self.URL_PROD = 'https://api-pix.gerencianet.com.br'

        self.KEY_PIX = ''

        self.headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }

    def verification_token(self):
        actual_date = datetime.timestamp(datetime.now())
        hour_expire = self.TIME
        if float(actual_date) >= float(hour_expire):
            token = self.get_token()
            self.headers['Authorization'] = f'Bearer {token}'
            self.TIME = datetime.timestamp(datetime.now()+timedelta(minutes=6))
        return

    def get_token(self):

        auth = base64.b64encode(
            (f'{self.CLIENT_ID}:{self.CLIENT_SECRET}').encode()).decode()
            
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        payload = {'grant_type': 'client_credentials'}
        response = requests.post(f'{self.URL_PROD}/oauth/token', headers=headers,
                                 data=json.dumps(payload), cert=self.CERTIFICATE)
        resp = response.json()
        if 'access_token' in resp:
            return resp['access_token']
        else:
            sleep(60)
            return self.get_token()

    def create_order(self, payload):

        self.verification_token()
        response = requests.post(f'{self.URL_PROD}/v2/cob', headers=self.headers,
                                 data=json.dumps(payload), cert=self.CERTIFICATE)
        if int(response.status_code) == 201:
            return response.json()
        return {}

    def update_order(self, txid):

        self.verification_token()
        response = requests.get(
            f'{self.URL_PROD}/v2/cob/{txid}', headers=self.headers, cert=self.CERTIFICATE)
        if response.status_code == 200:
            return response.json()
        return None

    def getQrCode(self, loc):

        qrcode = requests.get(
            f'{self.URL_PROD}/v2/loc/{loc}/qrcode', headers=self.headers, cert=self.CERTIFICATE)
        return qrcode.json()

    def qrCodeSave(self, data, txid):
        qrcode = pyqrcode.QRCode(data, error='H')
        qrcode.svg(f'./app/static/imgQr/qrcode-{txid}.svg')

    def create_charge(self, value):

        payload =  {"calendario": {"expiracao": 1440},
                            "valor": {"original":f'{value:.2f}'},
                            "chave": self.KEY_PIX,
                            "solicitacaoPagador": f"Recarga de R$ {str(value)} para o painel Números Virtuais."}

        data = self.create_order(payload)
        if len(data) > 0:
            loc = data.get('loc').get('id')
            qrcode:dict = self.getQrCode(loc)

            return qrcode.get('qrcode'), data.get('txid')

        return False
