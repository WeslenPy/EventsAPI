from app import app, db, mp_api
from flask import jsonify, request
from app.utils.functions import logging

from app.blueprints import v1

@v1.route('webhook/payment', methods=['POST'])
def webhook_mercadopago():
    data = request.get_json()

    logging.loggingFile('logWebhookPayment',[data])
    
    if "data" in data and "id" in data['data']:
        id_pagamento = data['data']['id']


    return jsonify({}),200
