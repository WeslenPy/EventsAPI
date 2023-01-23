from flask import Flask
from flask_restx import Api,Namespace

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

        self.authorizations = {
                'JWT': {
                    'type': 'apiKey',
                    "in": "header",
                    "name": "Authorization",
                }
        }

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
                        doc="/docs",
                        authorizations=self.authorizations,
                        security='JWT',
        )

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

        self.create_namespace()
        self.app.register_blueprint(self.api_v1)

        self.db.create_all()


    def create_namespace(self):

        self.admin_api =  Namespace("Admin",description="Routers of admin.",path="/admin")

        self.user_api = Namespace("User",description="Routers of user.",path="/user")
        self.category_api = Namespace("Category",description="Routers of category.",path='/category')
        self.events_api = Namespace("Events",description="Routers of events.",path='/event')
        self.lots_api = Namespace("Lots",description="Routers of lots.",path='/lot')
        self.orders_api = Namespace("Orders",description="Routers of orders.",path="/order")
        self.partner_api = Namespace("Partner",description="Routers of partner.",path='/partner')
        self.rules_api = Namespace("Rules",description="Routers of rules.",path="/rules")
        self.terms_api = Namespace("Terms",description="Routers of terms.",path="/terms")
        self.tickets_api = Namespace("Tickets",description="Routers of tickets.",path="/ticket")

        self.api.add_namespace(self.admin_api)
        self.api.add_namespace(self.user_api)
        self.api.add_namespace(self.events_api)
        self.api.add_namespace(self.category_api)
        self.api.add_namespace(self.orders_api)
        self.api.add_namespace(self.partner_api)
        self.api.add_namespace(self.rules_api)
        self.api.add_namespace(self.terms_api)
        self.api.add_namespace(self.tickets_api)


    def run(self):
        return self.app.run(debug=True)




app = App()