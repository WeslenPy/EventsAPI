

from app.databases.events.schema import EventSchema
from app.databases.events.models import Events
from werkzeug.datastructures import FileStorage
from flask_restx.inputs import datetime_from_iso8601
from app.utils.functions.decorators import auth
from marshmallow import ValidationError
from flask_restx import Resource
from app.server import app

api = app.events_api

event_parser = api.parser()
event_parser.add_argument('image', location='files',help="Imagem do evento.",
                           type=FileStorage, required=True)
event_parser.add_argument('video', location='files',help="Video do evento.",
                           type=FileStorage, required=True)

event_parser.add_argument('name', location='form',help="Nome do evento.",
                           type=str, required=True)
event_parser.add_argument('zip_code', location='form',help="Cep do evento.",
                           type=int, required=True)

event_parser.add_argument('state', location='form',help="Estado do evento.",
                           type=str, required=True)
event_parser.add_argument('address', location='form',help="Endereço do evento.",
                           type=str, required=True)

event_parser.add_argument('locale_name', location='form',help="Nome do local.",
                           type=str, required=True)   
event_parser.add_argument('number_address', location='form',help="Número do local do evento.",
                           type=int, required=True)   
event_parser.add_argument('complement', location='form',help="Complemento.",
                           type=str, required=True)   
event_parser.add_argument('district', location='form',help="Bairro.",
                           type=str, required=True)
                           
event_parser.add_argument('city', location='form',help="Cidade.",
                           type=str, required=True)                            
event_parser.add_argument('start_date', location='form',help="Data de inicio do evento.",
                           type=datetime_from_iso8601, required=True)                            
event_parser.add_argument('start_date', location='form',help="Data final do evento.",
                           type=datetime_from_iso8601, required=True)                            
event_parser.add_argument('start_hour', location='form',help="Horario de inicio.",
                           type=datetime_from_iso8601, required=True)     

event_parser.add_argument('category_id', location='form',help="Id da categoria do evento.",
                           type=int, required=True)                                                 
event_parser.add_argument('ticket_id', location='form',help="Id do ticket do evento.",
                           type=int, required=True)     
                                               
event_parser.add_argument('status', location='form',help="Status do termo.",
                           type=bool, required=False,default=True)


@api.route('/create')
class EventRouter(Resource):

    @api.expect(event_parser)
    @api.doc("Rota para cadastro do evento")
    @auth.authType(required=True,location='form')
    def post(self,**kwargs):
        data = event_parser.parse_args()
        _schema =  EventSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Event created successfully',
            'error':False},200



@api.route('/all')
class EventsRouter(Resource):

    @api.doc("Rota para pegar todos os eventos")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success")
    @auth.authType()
    def get(self,**kwargs):
        
        items = Events.query.filter_by(status=True).all()
        data = EventSchema(many=True).dump(items)

        return {"message":"Success","data":data,"code":200,"error":False},200


