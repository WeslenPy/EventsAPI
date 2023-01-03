from dotenv import load_dotenv
load_dotenv()

from os import environ


# SQLALCHEMY CONFIGS
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI','')
SQLALCHEMY_POOL_RECYCLE= int(environ.get('SQLALCHEMY_POOL_RECYCLE',299))
SQLALCHEMY_POOL_TIMEOUT= int(environ.get('SQLALCHEMY_POOL_TIMEOUT',20))
SQLALCHEMY_POOL_SIZE= int(environ.get('SQLALCHEMY_POOL_SIZE',300))
SQLALCHEMY_MAX_OVERFLOW= int(environ.get('SQLALCHEMY_MAX_OVERFLOW',500))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CONFIGURAÇÕES DO JSON PARA UTF-8
JSON_AS_ASCII = False
JSONIFY_PRETTYPRINT_REGULAR = True

# secret key para as sessões
SECRET_KEY = environ.get('SECRET_KEY','secret fuerte')

# configurações de email
MAIL_PORT = int(environ.get('MAIL_PORT',0))
MAIL_SERVER = environ.get('MAIL_SERVER','')
MAIL_USERNAME = environ.get('MAIL_USERNAME','')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD','')
MAIL_USE_TLS = False 
MAIL_USE_SSL = True 

# expiracao token em minutos
EXPIRATION_TOKEN = 180
TOKEN_SALT = "emailValidityAndConfirmToken"

#MERCADO PAGO API CONFIG
MP_ACCESS_PRIVATE_TOKEN = environ.get('MP_ACCESS_PRIVATE_TOKEN','')
MP_ACCESS_PUBLIC_TOKEN = environ.get('MP_ACCESS_PUBLIC_TOKEN','')

TESTING = False

# CONFIGURAÇÕES DO HOOK DO MERCADOPAGO
WEBHOOK_URL_CONFIGS = {
    "failure":environ.get('MP_WEBHOOK_URL_FAILURE',""),
    "pending":environ.get('MP_WEBHOOK_URL_PENDING',""),
    "success":environ.get('MP_WEBHOOK_URL_SUCCESS',""),
    "notify": environ.get('MP_WEBHOOK_URL_NOTIFY',"")
}



