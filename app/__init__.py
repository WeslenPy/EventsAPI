from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_executor import Executor
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flask import Flask

from .utils.functions.auth import GenerateJWT
from itsdangerous import URLSafeTimedSerializer
from api import MercadoPago,ApiBrasil
import boto3


app:Flask = Flask(__name__)
app.config.from_pyfile("config.py")

cors:CORS = CORS(app)
db:SQLAlchemy = SQLAlchemy(app)
ma:Marshmallow = Marshmallow(app)
migrate:Migrate = Migrate(app,db)

mp_api:MercadoPago = MercadoPago(app.config['MP_ACCESS_PRIVATE_TOKEN'],app.config['WEBHOOK_URL_CONFIGS'])
brasil_api:ApiBrasil = ApiBrasil()

mail:Mail = Mail(app)
tokenSafe:URLSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
executor:Executor = Executor(app)

s3:boto3.resource = boto3.resource('s3')
client_s3:boto3.client = boto3.client('s3')

jwt:GenerateJWT = GenerateJWT(app.config['SECRET_KEY'])

bucket_name = app.config['BUCKET_NAME']

from .routers import *
from .databases import *
from .blueprints import v1

db.create_all()
app.register_blueprint(blueprint=v1)