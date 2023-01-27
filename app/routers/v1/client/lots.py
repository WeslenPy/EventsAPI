from app.databases.events.schema import LotSchema
from app.databases.events.models import Lots
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app
from app.utils.functions.decorators import auth

api = app.lots_api

lot_model =api.model('Lot', {
    "quantity":fields.Integer(description='Quantidade do lote.',required=True,min=1),
    "price":fields.Float(description="Preço do ticket.",required=True,min=1),
    "start_date":fields.DateTime(description="Data de inicio do lote.",required=True),
    "end_date":fields.DateTime(description="Data de finalização do lote.",required=True),
    "ticket_id":fields.Integer(description="Id do ticket.",required=True),
    "status":fields.Boolean(description="Status do lote.",required=True,default=True),
    "created_at":fields.DateTime(description="Data de criação.",readonly=True),
})

lots_model = api.clone("Lots",app.default_model,{
    'data':fields.Nested(lot_model,description="Todos os lots cadastrados",as_list=True),
})

@api.route('/create')
class LotsRouter(Resource):

    @api.expect(lot_model)
    @api.doc("Rota para cadastro dos lotes")
    @auth.authType()
    def post(self,**kwargs):
        data = api.payload
        _schema =  LotSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Lot created successfully',
            'error':False},200


@api.route('/all')
class LotsRouter(Resource):

    @api.doc("Rota para pegar todos os lots")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success",lots_model)
    @auth.authType()
    def get(self,**kwargs):

        ticktes = Lots.query.filter_by(status=True).all()
        data = LotSchema(many=True).dump(ticktes)

        return {"message":"Success","data":data,"code":200,"error":False},200


