from .coinbaseOrder import makeOrderCoinbase
from .picpayOrder import makeOrderPicpay
from .pixOrder import makeOrderPix

from flask import jsonify


def createOrder(**kwargs):
    methodPayment = kwargs.get('method_name','')
    if methodPayment == 'pix':return makeOrderPix(**kwargs)
    elif methodPayment == 'picpay':return makeOrderPicpay(**kwargs)
    elif methodPayment == 'criptomoeda':return makeOrderCoinbase(**kwargs)
    else: return jsonify({'data':{},'message':'Método de pagamento é invalido.','error':1,'status':False})
        