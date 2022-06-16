from datetime import datetime

from flask import request,jsonify

from app.models import *
from app import app,db


@app.route('/webhook/coinbase/checkout',methods=['POST'])
def coinbaseCheckOut():

    WEBHOOK_SECRET = '10566334-a7cd-4356-9c58-fb87943ece23'
    request_data = request.data.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    try:
        event = Webhook.construct_event(request_data, request_sig, WEBHOOK_SECRET)

        txid_code = event['data']['code']
        status = event['data']['timeline'][-1]['status']

        methodCoinbase = PaymentMethod.query.filter_by(method='Criptomoeda').first().id

        order = RechargeHistory.query.filter_by(txid=txid_code,status='ACTIVE',
                                            payment_method_id=methodCoinbase).first()

        if order:
            user = User.query.get(order.user_id)
            if status in ['CONFIRMED', 'RESOLVED', 'COMPLETED']:
                user.balance += float(order.value)
                order.payday = datetime.now()
                order.status = 'CONCLUDED'

            elif status in 'CANCELED':
                order.status = 'CANCEL'            
            elif status in 'EXPIRED':
                order.status = 'EXPIRED'
    
            db.session.commit()

        return jsonify({'status':200}),200
    except:
        return jsonify({'status':404}),404
    

@app.route('/webhook/picpay/checkout',methods=['POST'])
def picpayCheckOut():
    token = request.headers.get("X-Seller-Token",False)
    if token and token == 'e330e4f8-7f11-42f9-86b2-298e32c25712':
        data = request.json
            
        methodPicpay = PaymentMethod.query.filter_by(method='Picpay').first().id
        order = RechargeHistory.query.filter_by(txid=data['referenceId'],status='ACTIVE',
                                                    payment_method_id=methodPicpay).first()

        if order:
            if 'authorizationId' in data:
                user = User.query.filter_by(id=order.user_id).first()
                user.balance +=float(order.value)
                order.payday = datetime.now()
                order.status = 'CONCLUDED'
            else:
                order.status = 'EXPIRED'
                
        db.session.commit()

        return jsonify({'status':200}),200
    
    return jsonify({'status':404}),404

@app.route('/webhook/pix/checkout/<method>',methods=['POST'])
def pixCheckOutWebHook(method):

    data = request.json
    if 'pix' not in data: return jsonify({'status':200}),200

    for pix in data['pix']:
        methodPix = PaymentMethod.query.filter_by(method='Pix').first().id
        recharge = RechargeHistory.query.filter_by(txid=pix['txid'],status='ACTIVE',
                                                    payment_method_id=methodPix).first()
      
        if recharge is None:continue

        recharge.status= "CONCLUDED"
        recharge.payday = datetime.now()
        userBalance = User.query.filter_by(id=recharge.user_id).first()
        userBalance.balance +=float(recharge.value)
        db.session.commit()

    return jsonify({'status':200}),200
