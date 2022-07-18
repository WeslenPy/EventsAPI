
from app.utils.functions import decorators
from flask import request,jsonify
from app import app,mp_api

from datetime import datetime
from app.models import Orders,Lots
from app.schema import OrderSchema



"""
POST REGISTER DATA 
"""

@app.route('/api/v1/create/order',methods=['POST'])
@decorators.authUserDecorator(required=True)
@decorators.validityDecorator({'lot_id':int,'quantity':int,"user_id":int})
def create_order():
    data = request.get_json()

    actual  =datetime.now()
    lotFind:Lots =Lots.query.filter_by(status=True,closed=False,id=data['lot_id']
                    ).first()

    if not lotFind:
        return jsonify({'status':400,'message':'Invalid lot_id','success':False}),200

    if lotFind.lot_children and len (lotFind.lot_children) >=lotFind.quantity:
        return jsonify({'status':400,'message':'available quantity',
                            'quantity':lotFind.quantity-len(lotFind.lot_children),'success':False}),200


    data = {'lot_id':lotFind.id,'user_id':data["user_id"],
                'method':'teste','value':lotFind.price,'quantity':data['quantity']}

    new:Orders = OrderSchema().load(data)
    new.save()

    order = OrderSchema().dump(new)
    order_generate = mp_api.create_preference(new.id,lotFind.price,quantity=new.quantity)

    return jsonify({'status':200,'message':'order created successfully',"data":order,'order':order_generate,'success':False}),200
    

# @app.route('/api/v1/get/genres',methods=['GET'])
# def get_genres():

#     genres:GenreTypes = GenreTypes.query.all()
#     genres = GenreTypeSchema(many=True).dump(genres)

#     return  jsonify({'status':200,'message':'success','data':genres,'success':True}),200

# @app.route('/api/v1/get/genre/<int:id_genre>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_genre(id_genre):

#     genre:GenreTypes = GenreTypes.query.get(id_genre)
#     genre = GenreTypeSchema().dump(genre)

#     return  jsonify({'status':200,'message':'success','data':genre,'success':True}),200

