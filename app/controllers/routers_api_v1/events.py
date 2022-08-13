
from app.utils.functions import decorators,validitys
from flask import request,jsonify
from datetime import datetime
from app import app,db

from app.models import Events,Category,Tickets
from app.schema import EventSchema


"""
POST REGISTER DATA 
"""
@app.route('/api/v1/create/event',methods=['POST'])
@decorators.authUserDecorator(required=True)
@decorators.validityDecorator({'name':str,'image':str,'video':str,'cep':int,'state':str,'address':str,
                                'number_address':int,'complement':str,'district':str,'city':str,'start_date':datetime,
                                'end_date':datetime,'status':bool,'category_id':int,'ticket_id':int,"user_id":int})
def create_event():

    data = request.json

    if not validitys.dateValidity(data['start_date'],data['end_date']):
        return jsonify({'status':400,'message':"Invalid end_date",'success':False}),400

    getCategory = Category.query.filter_by(id=data['category_id'],status=True).first()
    if not getCategory:return jsonify({'status':400,'message':"Invalid category_id",'success':False}),400

    getTicket:Tickets = Tickets.query.filter_by(id=data['ticket_id'],status=True).first()
    if not getTicket:return jsonify({'status':400,'message':"Invalid ticket_id",'success':False}),400

    if data['user_id'] != getTicket.user_id:
        return jsonify({'status':400,'message':"inaccessible event",'success':False}),400

    event:Events = EventSchema().load(data)
    event.save()

    eventData = EventSchema().dump(event)
    return jsonify({'status':200,'message':'event created successfully','data':eventData,'success':True}),200


"""
DELETE EVENT API DATA 
"""
@app.route('/api/v1/delete/event/<int:id_event>',methods=['DELETE'])
@decorators.authUserDecorator()
def delete_event(id_event):

    event:Events = Events.query.filter_by(id=id_event,status=False).first()
    if event:
        db.session.delete(event)
        db.session.commit()
    
        return  jsonify({'status':200,'message':'success','success':True}),200

    return  jsonify({'status':404,'message':'event not found or not eligible','success':False}),404



"""
GET DATA EVENT API
"""

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


