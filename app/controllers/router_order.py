from app.utils.functions import decorators,not_found,create_order
from flask import request,jsonify
from app.models import *
from app.schema import *
from app import app,db
from time import time


@app.route('/payments/history',methods=['POST'])
@decorators.authUserDecorator(True)
def getHistoric(currentUser):

        historyAll = RechargeHistory.query.filter_by(user_id=currentUser['some']['id']).order_by(RechargeHistory.created_at.desc()).join(PaymentMethod,PaymentMethod.id==RechargeHistory.payment_method_id).add_columns(
            RechargeHistory.id,RechargeHistory.created_at,RechargeHistory.expiration,
            RechargeHistory.value,RechargeHistory.status,PaymentMethod.method,RechargeHistory.url).all()

        result = not_found.checkContent(historyAll)
        if result !=False:return result

        for payment in historyAll:
            if payment.status =='ACTIVE':
                if time() >= float(payment.expiration):
                    historic = RechargeHistory.query.get(payment.id)
                    historic.status = 'EXPIRED'

        db.session.commit()
        historyAll = HistoryPaymentSchema(many=True).dump(historyAll)

        return jsonify({'data':historyAll,'error':0,'message':'success','status':True}),200


@app.route('/get_order',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({'method':str,'idPayment':int})
def getOrder(currentUser):

    dataResponse = request.json

    method_payment = PaymentMethod.query.filter_by(method=dataResponse['method']).first()
    paymentPix = RechargeHistory.query.filter_by(id=dataResponse['idPayment'],user_id=currentUser['some']['id'],
                                            payment_method_id=method_payment.id,status='ACTIVE'
                                            ).order_by(RechargeHistory.id.asc()).first()

    result = not_found.checkContent(paymentPix)
    if result !=False:return result

    if time() >= float(paymentPix.expiration):
        paymentPix.status = 'EXPIRED'
        db.session.commit()
        return jsonify({'data':{},'error':1,'message':'Pedido expirado.','status':False})

    source=''
    value = f'{float(str(paymentPix.value).replace(",",".")):.2f}'.replace(".",",")
    if method_payment.method.lower() =='pix':
        source = pyqrcode.QRCode(paymentPix.obs,error='H').png_as_base64_str(scale=5)

    return jsonify({'data':{'b64image':source,'qrcode':paymentPix.obs,'value':value,
                                    'expiration':paymentPix.expiration},
                                    'error':0,'message':'success','status':True}),200


@app.route('/payment_order',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({'method':str,'value':[float,str]})
def paymentOrder(currentUser):
        dataResponse = request.json
        value = dataResponse['value']
        methodPayment = dataResponse['method']

        value = float(str(value).replace(',','.'))

        if value < 7.20:
            return jsonify({'data':{},'error':1,'message':'Valor minimo é R$ 7,20','status':False})

        findMethod = PaymentMethod.query.filter_by(method=methodPayment).first()

        if findMethod:
            methodPayment = methodPayment.lower()
            user_id = currentUser['some']['id']
            return create_order.createOrder(value=value,method_id=findMethod.id,user_id=user_id,method_name=methodPayment)

        return jsonify({'data':{},'message':'Método de pagamento é invalido.','error':1,'status':False})

