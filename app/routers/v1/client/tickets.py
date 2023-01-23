from app.databases.events.schema import TicketSchema
from app.utils.functions.decorators import auth
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app

api = app.tickets_api

ticket_model =api.model('Tickets', {
    "title":fields.String(description='Titulo do ticket.',required=True,),
    "price":fields.Float(description="Preço do ticket.",required=True,min=1),
    "description":fields.String(description="Descrição do ticket.",required=False,default=''),
    "max_buy":fields.Integer(description="Quantidade maximo do ticket.",required=True,min=1),
    "min_buy":fields.Integer(description="Quantidade minima do ticket.",required=True,min=1),
    "paid":fields.Boolean(description="Ticket pago.",required=True,default=True),
    "status":fields.Boolean(description="Status do ticket.",required=True,default=True),
    "created_at":fields.DateTime(description="Data de criação.",readonly=True),
})
@api.route('/create')
class Tickets(Resource):

    @api.expect(ticket_model)
    @api.doc("Rota para cadastro dos tickets")
    @auth.authType(required=True,api=api)
    def post(self,**kwargs):
        data = api.payload
        _schema =  TicketSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'status':200,
            'message':'Ticket created successfully',
            'error':False},200


    

# from app.utils.functions import decorators
# from flask import request,jsonify
# from app import app

# from app.databases.events.schema  import TicketSchema
# from app.databases.events.models    import Tickets

# from app.blueprints import v1

# """
# POST REGISTER DATA 
# """

# @v1.route('create/ticket',methods=['POST'])
# @decorators.authUserDecorator(required=True)
# @decorators.validityDecorator({'title':str,'description':str,"user_id":int,"price":[float,int],
#                             'max_buy':int,'min_buy':int,'paid':bool,'status':bool})
# def create_ticket():

#     data = request.get_json()
#     ticket:Tickets =TicketSchema().load(data)
#     ticket.save()

#     ticketData = TicketSchema().dump(ticket)
#     return jsonify({'status':200,'message':'ticket created successfully','data':ticketData,'success':True}),200


# @v1.route('get/tickets',methods=['GET'])
# @decorators.authUserDecorator()
# def get_tickets():

#     tickets:Tickets = Tickets.query.all()
#     tickets = TicketSchema(many=True).dump(tickets)

#     return  jsonify({'status':200,'message':'success','data':tickets,'success':True}),200
    
# @v1.route('get/ticket/<int:id_ticket>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_ticket(id_ticket):

#     ticket:Tickets = Tickets.query.get(id_ticket)
#     ticket = TicketSchema().dump(ticket)

#     return  jsonify({'status':200,'message':'success','data':ticket,'success':True}),200