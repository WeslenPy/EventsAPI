from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_executor import Executor
from flask_migrate import Migrate

from app.api import MercadoPago

from .auth import GenerateJWT

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:54U*%HGihgiGY#$Q@localhost/StorageDev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Weslen:54U*%HGihgiGY#$Q@Weslen.mysql.pythonanywhere-services.com/Weslen$StorageDev'
app.config['SECRET_KEY'] = '54U*%HGihgiGY#$Q@54U*%HGihgiGY#$Q54U*%HGihgiGY#$Q54U*%HGihgiGY#$Q'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_POOL_SIZE'] = 300
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 500

app.config['ACCESS_TOKEN_MP'] = 'TEST-4513928861865954-052023-043a8e8938961fade859e08f1592cc24-1125082385'
app.config['WEBHOOKS_URLS_MP'] = {
    "failure":"https://weslen.pythonanywhere.com/webhook/failure",
    "pending":"https://weslen.pythonanywhere.com/webhook/pending",
    "success":"https://weslen.pythonanywhere.com/webhook/success",
    "notify":"https://weslen.pythonanywhere.com/webhook/notify"
}


app.config['CORS_HEADERS'] = 'Content-Type'

app.config['MAIL_PORT'] = 465
app.config['MAIL_SERVER'] = 'mail.meunumerovirtual.com'
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_USERNAME'] = 'noreply@meunumerovirtual.com'
app.config['MAIL_PASSWORD'] = '290819943@kel'

cors = CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)

mp_api = MercadoPago(app.config['ACCESS_TOKEN_MP'],app.config['WEBHOOKS_URLS_MP'])

mail = Mail(app)
tokenSafe = URLSafeTimedSerializer(app.config['SECRET_KEY'])
executor = Executor(app)

jwtGen = GenerateJWT(app.config['SECRET_KEY'])

db.create_all()
# db.session.execute("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
# db.session.execute("SET GLOBAL max_connections = 6000;")
# db.session.commit()

from .controllers.routers_api import *
