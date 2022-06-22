
from app.utils.functions import decorators
from flask import request,jsonify
from datetime import datetime
from app import app

from app.models import Events,Category,Tickets
from app.schema import EventSchema

"""
POST REGISTER DATA 
"""
@app.route('/api/v1/create/event',methods=['POST'])
@decorators.authUserDecorator(required=True)
@decorators.validityDecorator({'name':str,'image':str,'video':str,'cep':int,'state':str,'address':str,
                                'number_address':int,'complement':str,'district':str,'city':str,'start_date':datetime,
                                'end_date':datetime,'status':bool,'category_id':int,'ticket_id':int,'user_id':int})
def create_event():

    data = request.json

    getCategory = Category.query.filter_by(id=data['category_id'],status=True).first()
    if not getCategory:return jsonify({'status':200,'message':"Invalid category_id",'success':True}),200

    getTicket= Tickets.query.filter_by(id=data['ticket_id'],status=True).first()
    if not getTicket:return jsonify({'status':200,'message':"Invalid ticket_id",'success':True}),200

    event:Events = EventSchema().load(data)
    event.save()

    eventData = EventSchema().dump(event)
    return jsonify({'status':200,'message':'event created successfully','data':eventData,'success':True}),200
    

@app.route('/api/v1/get/events',methods=['GET'])
@decorators.authUserDecorator()
def get_events():

    events:Events = Events.query.all()
    events = EventSchema(many=True).dump(events)

    return  jsonify({'status':200,'message':'success','data':events,'success':True}),200


@app.route('/api/v1/get/event/<int:id_event>',methods=['GET'])
@decorators.authUserDecorator()
def get_event(id_event):

    event:Events = Events.query.get(id_event)
    event = EventSchema().dump(event)

    return  jsonify({'status':200,'message':'success','data':event,'success':True}),200
