from app import app, db, mpapi
from flask import jsonify, request


@app.route('/api/v1/webhook/payment', methods=['POST'])
def webhook_mercadopago():
    data = request.get_json()
    
    if "data" in data and "id" in data['data']:
        id_pagamento = data['data']['id']

        data_payment = mpapi.get_payment_info(id_pagamento)
        if not data_payment:
            return jsonify({"status":200}),200

        if "status" in data_payment:
            status = data_payment['status']

            if "approved" not in data_payment['status']:
                data_payment = mpapi.get_payment_info(id_pagamento)
                if not data_payment:
                    return jsonify({"status":200}),200


            if "approved" in data_payment['status']:
                id_pedido = data_payment['additional_info']["items"][0]['id']
                meio_pagamento = data_payment['payment_method_id']
                email_pagamento = data_payment['payer']['email']


    return jsonify({}) ,200
