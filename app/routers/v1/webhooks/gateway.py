from app.server.instance import app
from flask import request


# @app.route('webhook/payment', methods=['POST'])
# def webhook_mercadopago():
#     data = request.get_json()

#     if "data" in data and "id" in data['data']:
#         id_pagamento = data['data']['id']


#     return jsonify({}),200
