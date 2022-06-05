from flask import jsonify
from app.models import User,RechargeHistory
from app.api import Picpay
from app import db

def makeOrderPicpay(value,user_id,method_id,method_name):

    userPayment = User.query.filter_by(id=user_id).first()

    if userPayment.cpf is None:
        return jsonify({'data':{},'status':False,
                        'message':'Cadastre seu CPF em seu perfil para conseguir recarregar via PicPay',
                        'error':1}),404

    orderPicpay = Picpay().create_order(value,userPayment.cpf)

    if orderPicpay !=False:
        url,code =orderPicpay

        picpayRecharge = RechargeHistory(txid=str(code),value=float(value),user_id=user_id,
                                    payment_method_id=method_id,obs='Release',url=url)
        db.session.add(picpayRecharge)
        db.session.commit()

        idPayment = RechargeHistory.query.filter_by(user_id=user_id,
                            payment_method_id=method_id,txid=str(code)).order_by(
                                RechargeHistory.id.desc()).first()

        return jsonify({'data':{'idPayment':idPayment.id,'method':method_name},
                        'url':url, 'message':'success','error':0,'status':True}),200

    return jsonify({'data':{},'status':False,'message':'Erro ao gerar cobrança','error':1}),301
