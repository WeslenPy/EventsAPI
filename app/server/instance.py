from flask import Flask
from flask_restx import Api

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_executor import Executor
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flask import Flask,Blueprint

from ..utils.functions.auth import GenerateJWT
from itsdangerous import URLSafeTimedSerializer
from api import MercadoPago,ApiBrasil
import boto3


class App:
    def __init__(self):
        self.app:Flask = Flask(__name__)
        self.app.config.from_pyfile("config.py")

        self.api_v1 =Blueprint(
                    name = 'api_v1', 
                    import_name = __name__, 
                    url_prefix='/api/v1')

        
        self.api:Api = Api(self.api_v1,
                        version='1.0',
                        title="Moderna Pass API",
                        description="API para venda de ingressos",
                        doc="/docs")


        self.cors:CORS = CORS(self.app)
        self.db:SQLAlchemy = SQLAlchemy(self.app)
        self.ma:Marshmallow = Marshmallow(self.app)
        self.migrate:Migrate = Migrate(self.app,self.db)

        self.mp_api:MercadoPago = MercadoPago(self.app.config['MP_ACCESS_PRIVATE_TOKEN'],self.app.config['WEBHOOK_URL_CONFIGS'])
        self.brasil_api:ApiBrasil = ApiBrasil()

        self.mail:Mail = Mail(self.app)
        self.tokenSafe:URLSafeTimedSerializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])
        self.executor:Executor = Executor(self.app)

        self.s3:boto3.resource = boto3.resource('s3')
        self.client_s3:boto3.client = boto3.client('s3')

        self.jwt:GenerateJWT = GenerateJWT(self.app.config['SECRET_KEY'])

        self.bucket_name:str = self.app.config['BUCKET_NAME']

        self.app.register_blueprint(self.api_v1)


    def run(self):
        return self.app.run(debug=True)




app = App()