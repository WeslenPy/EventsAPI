

from app.databases.events.schema import EventSchema
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
class Event(Resource):

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



# """
# POST REGISTER DATA 
# """
# @v1.route('create/event',methods=['POST'])
# @decorators.authUserDecorator(param=True)
# @decorators.validityDecoratorForm(['name','image','video','cep','state','address',"locale_name",
#                                 'number_address','complement','district','city','start_date',"start_hour",
#                                 'end_date','status','category_id','ticket_id','user_id'])
# def create_event(currentUser,data):

#     if not validitys.dateValidity(data['start_date'],data['end_date'],data['start_hour'],format="%Y-%m-%dT%H:%M:%S.%fZ"):
#         return jsonify({'status':400,'message':"Invalid datetime format",'success':False}),400

#     getCategory = Category.query.filter_by(id=data['category_id'],status=True).first()
#     if not getCategory:return jsonify({'status':400,'message':"Invalid category_id",'success':False}),400

#     getTicket:Tickets = Tickets.query.filter_by(id=data['ticket_id'],user_id=data['user_id'],status=True).first()
#     if not getTicket:return jsonify({'status':400,'message':"Invalid ticket_id",'success':False}),400

#     image,image_filename= data['image'],secure_filename(data['image'].filename)
#     video,video_filename = data['video'],secure_filename(data['video'].filename)

#     data["image"] = aws.upload_file(image,image_filename)
#     data["video"] =  aws.upload_file(video,video_filename)

#     try:
#         event:Events = EventSchema().load(data)
#         event.save()
        
#     except ValidationError as err: 
#         message = error_messages.parseMessage(err.messages)
#         return jsonify({'status':400,'message':message,'success':False}),400

#     eventData = EventSchema().dump(event)
#     return jsonify({'status':200,'message':'event created successfully','data':eventData,'success':True}),200


# """
# DELETE EVENT API DATA 
# """
# @v1.route('delete/event/<int:id_event>',methods=['DELETE'])
# @decorators.authUserDecorator()
# def delete_event(id_event):

#     event:Events = Events.query.filter_by(id=id_event,status=False).first()
#     if event:
#         db.session.delete(event)
#         db.session.commit()
    
#         return  jsonify({'status':200,'message':'success','success':True}),200

#     return  jsonify({'status':404,'message':'event not found or not eligible','success':False}),404



# """
# GET DATA EVENT API
# """

# @v1.route('get/events',methods=['GET'])
# @decorators.authUserDecorator()
# def get_events():

#     events:Events = Events.query.all()
#     events = EventSchema(many=True).dump(events)

#     return  jsonify({'status':200,'message':'success','data':events,'success':True}),200


# @v1.route('get/event/<int:id_event>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_event(id_event):

#     event:Events = Events.query.get(id_event)
#     event = EventSchema().dump(event)

#     return  jsonify({'status':200,'message':'success','data':event,'success':True}),200


