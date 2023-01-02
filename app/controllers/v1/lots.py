
from app.utils.functions import decorators,validitys
from flask import request,jsonify
from datetime import datetime
from app import app

from app.databases.events.models    import Lots,Tickets,Users
from app.databases.events.schema  import LotSchema

from app.blueprints import v1

"""
POST REGISTER DATA 
"""

@v1.route('create/lot',methods=['POST'])
@decorators.authUserDecorator(required=True)
@decorators.validityDecorator({'quantity':int,'price':[float,int],'start_date':datetime,"user_id":int,
                                "end_date":datetime,'ticket_lot_id':int,'status':bool})
def create_lot():

    data = request.get_json()

    if not validitys.dateValidity(data['start_date'],data['end_date']):
        return jsonify({'status':400,'message':"Invalid end_date",'success':False}),400

    findTicket:Tickets = Tickets.query.get(data['ticket_lot_id'])
    if not findTicket:
        return jsonify({'status':400,'message':'invalid ticket_lot_id','success':False}),200

    if data['user_id'] != findTicket.user_id:
        return jsonify({'status':404,'message':"event not found",'success':False}),404


    new_lot:Lots = LotSchema().load(data)
    new_lot.save()

    lotData = LotSchema().dump(new_lot)
    return jsonify({'status':200,'message':'lot created successfully','data':lotData,'success':True}),200

    

@v1.route('get/lots',methods=['GET'])
@decorators.authUserDecorator()
def get_lots():

    lots:Lots = Lots.query.all()
    lots = LotSchema(many=True).dump(lots)

    return  jsonify({'status':200,'message':'success','data':lots,'success':True}),200


@v1.route('get/lot/<int:id_lot>',methods=['GET'])
@decorators.authUserDecorator()
def get_lot(id_lot):

    lot:Lots = Lots.query.get(id_lot)
    lot = LotSchema().dump(lot)

    return  jsonify({'status':200,'message':'success','data':lot,'success':True}),200
    