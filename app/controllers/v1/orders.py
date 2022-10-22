
from app.utils.functions import decorators
from flask import request,jsonify
from app import app,mp_api

from datetime import datetime
from app.database.models    import Orders,Lots
from app.database.schema  import OrderSchema



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
    

@app.route('/api/v1/get/orders',methods=['GET'])
@decorators.authUserDecorator(param=True)
def get_orders(currentUser):

    orders:Orders = Orders.query.filter_by(user_id=currentUser).all()
    orders = OrderSchema(many=True).dump(orders)

    return  jsonify({'status':200,'message':'success','data':orders,'success':True}),200

@app.route('/api/v1/get/order/<int:id_order>',methods=['GET'])
@decorators.authUserDecorator(param=True)
def get_order(id_order,currentUser):

    order:Orders = Orders.query.filter_by(user_id=currentUser).get(id_order)
    order = OrderSchema().dump(order)

    return  jsonify({'status':200,'message':'success','data':order,'success':True}),200

