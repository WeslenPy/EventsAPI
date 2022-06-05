from flask import jsonify
from app.models import RechargeHistory
from app.api import Coinbase
from app import db

def makeOrderCoinbase(value,user_id,method_id,method_name):

    if value < 30: return jsonify({'data':{},'error':1,
                                            'message':'Valor minimo para Criptomoeda é R$ 30,00',
                                            'status':False})

    data= Coinbase().create_order(float(value))
    if data ==False:
        return jsonify({'data':{},'status':False,'message':'Erro ao gerar cobrança','error':1})

    code,url = data

    bitcoinRecharge = RechargeHistory(txid=str(code),value=float(value),expiration={"hours":2},
                                user_id=user_id,payment_method_id=method_id,
                                obs='Release',url=url)

    db.session.add(bitcoinRecharge)
    db.session.commit()

    idPayment = RechargeHistory.query.filter_by(user_id=user_id,
                                    payment_method_id=method_id,txid=str(code)).order_by(
                                            RechargeHistory.id.desc()).first()

    return jsonify({'data':{'idPayment':idPayment.id,'method':method_name},
                    'url':url, 'message':'success','error':0,'status':True})