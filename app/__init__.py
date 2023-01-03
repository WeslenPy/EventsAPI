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


app = Flask(__name__)
app.config.from_pyfile("config.py")

cors = CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)

mp_api = MercadoPago(app.config['MP_ACCESS_PRIVATE_TOKEN'],app.config['WEBHOOK_URL_CONFIGS'])
brasil_api = ApiBrasil()

mail = Mail(app)
tokenSafe = URLSafeTimedSerializer(app.config['SECRET_KEY'])
executor = Executor(app)

s3 = boto3.resource('s3')
client_s3 = boto3.client('s3')

jwt:GenerateJWT = GenerateJWT(app.config['SECRET_KEY'])

db.create_all()

from .routers import *
from .blueprints import v1


app.register_blueprint(blueprint=v1)