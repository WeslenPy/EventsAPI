from app.databases.events.schema import TicketSchema
from app.databases.events.models import Tickets
from app.utils.functions.decorators import auth
from flask_restx import Resource,fields,Namespace
from marshmallow import ValidationError
from app.server import app

api:Namespace = app.tickets_api

ticket_model =api.model('Ticket', {
    "title":fields.String(description='Titulo do ticket.',required=True,),
    "price":fields.Float(description="Preço do ticket.",required=True,min=1),
    "description":fields.String(description="Descrição do ticket.",required=False,default=''),
    "max_buy":fields.Integer(description="Quantidade maxima do ticket.",required=True,min=1),
    "min_buy":fields.Integer(description="Quantidade minima do ticket.",required=True,min=1),
    "paid":fields.Boolean(description="Ticket pago.",required=True,default=True),
    "status":fields.Boolean(description="Status do ticket.",required=True,default=True),
    "created_at":fields.DateTime(description="Data de criação.",readonly=True),
    "user_id":fields.Integer(description="Id do usuario.",readonly=True),
})

tickets_model = api.clone("Tickets",app.default_model,{
    'data':fields.Nested(ticket_model,description="Todos os tickets cadastrados",as_list=True),
})


@api.route('/create')
class Tickets(Resource):

    @api.expect(ticket_model)
    @api.doc("Rota para cadastro dos tickets")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success",app.default_model)
    @auth.authType(required=True,api=api)
    def post(self,**kwargs):
        data = api.payload
        _schema =  TicketSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},400

        return {
            'code':200,
            'message':'Ticket created successfully',
            'error':False},200

@api.route('/all')
class TicketsAll(Resource):

    @api.doc("Rota para pegar todos os tickets")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success",tickets_model)
    @auth.authType(required=True)
    def get(self,**kwargs):
        ticktes = Tickets.query.filter_by(user_id=kwargs['user_id'],status=True).all()
        data = TicketSchema(many=True).dump(ticktes)

        return data,200


