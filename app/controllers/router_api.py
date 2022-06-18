from flask import request,jsonify
from datetime import datetime,timedelta
from app.schema.ticketSchema import TicketSchema
from app.utils.functions import decorators
from app import app
from app.models import *
from app.schema import *

"""
POST REGISTER DATA 
"""
@app.route('/api/v1/create/event',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'name':str,'image':str,'video':str,'cep':str,'state':str,'address':str,
                                'number_address':int,'complement':str,'district':str,'city':str,"start_date":[str,datetime],
                                'end_date':[str,datetime],'status':bool,"category_id":int})
def create_event():
    data = request.get_json()
    event:Events = EventSchema().load(data)
    event.save()

    eventData = EventSchema().dump(event)
    return jsonify({'status':200,'message':'event created successfully','data':eventData,'success':True}),200
    

@app.route('/api/v1/create/ticket',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'title':str,'description':str,'max_buy':int,'min_buy':int,'paid':bool})
def create_ticket():
    data = request.get_json()
    ticket:Tickets =TicketSchema().load(data)
    ticket.save()

    ticketData = TicketSchema().dump(ticket)
    return jsonify({'status':200,'message':'ticket created successfully','data':ticketData,'success':True}),200


@app.route('/api/v1/create/genre',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'type':str,'description':str})
def create_genre():
    data = request.get_json()

    genreFind =GenreTypes.query.filter(GenreTypes.type==data['type']).first()
    if not genreFind:
        genre:GenreTypes = GenreTypeSchema().load(data)
        genre.save()

        genreData = GenreTypeSchema().dump(genre)
        return jsonify({'status':200,'message':'genre created successfully','data':genreData,'success':True}),200

    genreData = GenreTypeSchema().dump(genreFind)
    return jsonify({'status':200,'message':'genre has already been registered','data':genreData,'success':False}),200
    
   
@app.route('/api/v1/create/category',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'name':str,'description':str})
def create_category():
    data = request.get_json()
    
    categoryFind =Category.query.filter_by(name=data['name']).first()
    if not categoryFind:
        new_category:Category = CategorySchema().load(data)
        new_category.save()

        categoryData = CategorySchema().dump(new_category)
        return jsonify({'status':200,'message':'category created successfully','data':categoryData,'success':True}),200
    
    categoryData = CategorySchema().dump(categoryFind)
    return jsonify({'status':200,'message':'category has already been registered','data':categoryData,'success':False}),200
    

@app.route('/api/v1/create/lot',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'quantity':int,'price':[float,int],'start_date':datetime,
                                "end_date":datetime,'ticket_id':int,'status':bool})
def create_lot():
    data = request.get_json()
    
    new_lot:Lots = LotSchema().load(data)
    new_lot.save()

    lotData = LotSchema().dump(new_lot)
    return jsonify({'status':200,'message':'lot created successfully','data':lotData,'success':True}),200

    


"""
GET API DATA ALL
"""

@app.route('/api/v1/get/users',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_users():

    users:Users = Users.query.all()
    users = UserSchema(many=True).dump(users)

    return  jsonify({'status':200,'message':'success','data':users,'success':True}),200
    
@app.route('/api/v1/get/lots',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_lots():

    lots:Lots = Lots.query.all()
    lots = LotSchema(many=True).dump(lots)

    return  jsonify({'status':200,'message':'success','data':lots,'success':True}),200
    

@app.route('/api/v1/get/genres',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_genres():

    genres:GenreTypes = GenreTypes.query.all()
    genres = GenreTypeSchema(many=True).dump(genres)

    return  jsonify({'status':200,'message':'success','data':genres,'success':True}),200


@app.route('/api/v1/get/categorys',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_categorys():

    categorys:Category = Category.query.all()
    categorys = CategorySchema(many=True).dump(categorys)

    return  jsonify({'status':200,'message':'success','data':categorys,'success':True}),200


@app.route('/api/v1/get/events',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_events():

    events:Events = Events.query.all()
    events = EventSchema(many=True).dump(events)

    return  jsonify({'status':200,'message':'success','data':events,'success':True}),200


@app.route('/api/v1/get/tickets',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_tickets():

    tickets:Tickets = Tickets.query.all()
    tickets = TicketSchema(many=True).dump(tickets)

    return  jsonify({'status':200,'message':'success','data':tickets,'success':True}),200