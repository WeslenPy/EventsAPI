
from app.utils.functions import decorators
from flask import request,jsonify
from datetime import datetime
from app import app

from app.models import Lots
from app.schema import LotSchema


"""
POST REGISTER DATA 
"""

@app.route('/api/v1/create/lot',methods=['POST'])
@decorators.authUserDecorator()
@decorators.validityDecorator({'quantity':int,'price':[float,int],'start_date':datetime,
                                "end_date":datetime,'ticket_id':int,'status':str})
def create_lot():


    data = request.get_json()
    if data['status'] not in ('ACTIVE','DISABLED'):
        return jsonify({'status':400,'message':'missing or invalid field','json_error':False,
                            'details':{'param':'status','invalid_type':True,'invalid_param':False},'success':False}),200
    
    new_lot:Lots = LotSchema().load(data)
    new_lot.save()

    lotData = LotSchema().dump(new_lot)
    return jsonify({'status':200,'message':'lot created successfully','data':lotData,'success':True}),200

    

@app.route('/api/v1/get/lots',methods=['GET'])
@decorators.authUserDecorator()
def get_lots():

    lots:Lots = Lots.query.all()
    lots = LotSchema(many=True).dump(lots)

    return  jsonify({'status':200,'message':'success','data':lots,'success':True}),200


@app.route('/api/v1/get/lot/<int:id_lot>',methods=['GET'])
@decorators.authUserDecorator()
def get_lot(id_lot):

    lot:Lots = Lots.query.get(id_lot)
    lot = LotSchema().dump(lot)

    return  jsonify({'status':200,'message':'success','data':lot,'success':True}),200
    