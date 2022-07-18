from app import app, db, mp_api
from flask import jsonify, request


@app.route('/api/v1/webhook/payment', methods=['POST'])
def webhook_mercadopago():
    data = request.get_json()
    
    if "data" in data and "id" in data['data']:
        id_pagamento = data['data']['id']



    return jsonify({}) ,200
