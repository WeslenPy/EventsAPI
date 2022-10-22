from flask import jsonify

from app import app,db,s3
from app.utils.functions import decorators,validitys,error_messages,get_url
from app.database.models    import Events,Category,Tickets
from app.database.schema  import EventSchema

from marshmallow import ValidationError
from werkzeug.utils import secure_filename


"""
POST REGISTER DATA 
"""
@app.route('/api/v1/create/event',methods=['POST'])
@decorators.authUserDecorator(param=True)
@decorators.validityDecoratorForm(['name','image','video','cep','state','address',"locale_name",
                                'number_address','complement','district','city','start_date',
                                'end_date','status','category_id','ticket_id','user_id'])
def create_event(currentUser,data):

    if not validitys.dateValidity(data['start_date'],data['end_date'],format="%Y-%m-%dT%H:%M:%S.%fZ"):
        return jsonify({'status':400,'message':"Invalid end_date",'success':False}),400

    getCategory = Category.query.filter_by(id=data['category_id'],status=True).first()
    if not getCategory:return jsonify({'status':400,'message':"Invalid category_id",'success':False}),400

    getTicket:Tickets = Tickets.query.filter_by(id=data['ticket_id'],status=True).first()
    if not getTicket:return jsonify({'status':400,'message':"Invalid ticket_id",'success':False}),400

    if data['user_id'] != getTicket.user_id:
        return jsonify({'status':400,'message':"inaccessible event",'success':False}),400

    image,image_filename= data['image'],secure_filename(data['image'].filename)
    video,video_filename = data['video'],secure_filename(data['video'].filename)

    bucket_name = 'moderna-pass'
    bucket = s3.Bucket(bucket_name)

    bucket.upload_fileobj(image,image_filename)
    bucket.upload_fileobj(video,video_filename)

    data["image"] = get_url.generate_uri(bucket_name,image_filename)
    data["video"] =  get_url.generate_uri(bucket_name,image_filename)

    try:
        event:Events = EventSchema().load(data)
        event.save()
        
    except ValidationError as err: 
        message = error_messages.parseMessage(err.messages)
        return jsonify({'status':400,'message':message,'success':False}),400

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


