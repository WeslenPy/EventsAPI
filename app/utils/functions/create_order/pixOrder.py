from app.models import RechargeHistory
from app.api import Pix
from flask import jsonify
from app import db
import pyqrcode

def makeOrderPix(value,user_id,method_id,method_name):

    pix = Pix()
    dataPix = pix.create_charge(value)
    if dataPix !=False:
        qrcode,txid = dataPix

        url_redirect = "pix/payment'"

        pixRecharge = RechargeHistory(txid=str(txid),value=float(value),user_id=user_id,
                                        payment_method_id=method_id,obs=str(qrcode),url=url_redirect)
        db.session.add(pixRecharge)
        db.session.commit()

        idPayment = RechargeHistory.query.filter_by(user_id=user_id,
                                                    payment_method_id=method_id,
                                                    txid=str(txid)).order_by(
                                                        RechargeHistory.id.desc()).first()


        b64image = pyqrcode.QRCode(str(qrcode),error='H').png_as_base64_str(scale=5)

        return jsonify({'data':{'idPayment':idPayment.id,
                                    'qrcode':str(qrcode),'b64qrcode':b64image,
                                        'method':method_name},
                                            'url':url_redirect, 
                                                'message':'QRCode pix gerado com sucesso.',
                                                    'error':0,'status':True})

    return jsonify({"data":'','status':False,'error':1,'message':'Erro ao gerar cobrança.'})
