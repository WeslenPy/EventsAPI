from flask import request,jsonify
from datetime import datetime,timedelta
from app.schema.ticketSchema import TicketSchema
from app.utils.functions import decorators
from app import app
from app.models import *
from app.schema import *



@app.route('/api/v1/create/event',methods=['POST'])
@decorators.authUserDecorator(is_admin=True)
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
@decorators.authUserDecorator(is_admin=True)
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
    genre:GenreTypes = GenreTypeSchema().load(data)
    genre.save()

    genreData = GenreTypeSchema().dump(genre)
    return jsonify({'status':200,'message':'genre created successfully','data':genreData,'success':True}),200

   
@app.route('/api/v1/create/category',methods=['POST'])
@decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'name':str,'description':str})
def create_category():
    data = request.get_json()
    new_category:Category = CategorySchema().load(data)
    new_category.save()

    categoryData = CategorySchema().dump(new_category)
    return jsonify({'status':200,'message':'category created successfully','data':categoryData,'success':True}),200


   