from app.databases.events.schema import OrderSchema
from app.databases.events.models import Orders
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app
from app.utils.functions.decorators import auth
from api.mp_api import MercadoPago

api = app.orders_api

order_model =api.model('Order', {
    "lot_id":fields.Integer(description="Id do lot.",required=True),
    "quantity":fields.Integer(description="Quantidade de tickets",required=True,default=1,min=1),
    "user_id":fields.Integer(description="Id do usuário.",readonly=True),
})

orders_model = api.clone("Orders",app.default_model,{
    'data':fields.Nested(order_model,description="Todos os pedidos.",as_list=True),
})

@api.route('/create')
class OrderRouter(Resource):

    @api.expect(order_model)
    @api.doc("Rota para gerar pedido")
    @auth.authType(required=True,api=api)
    def post(self,**kwargs):
        data = api.payload
        _schema =  OrderSchema()

        try:data:Orders= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.","code":400,
                                "details":{"erros":erros.messages}},400

        mp:MercadoPago = app.mp_api

        preference = mp.create_preference(data.id,data.unit_price,
                                        quantity=data.quantity).get('id','')

        return {
            'code':200,
            'message':'Order created successfully',
            "preference_id":preference,
            'error':False},200


