
from app.utils.functions import decorators
from flask import request,jsonify
from datetime import datetime
from app import app

from app.schema import TicketSchema
from app.models import Tickets

"""
POST REGISTER DATA 
"""

@app.route('/api/v1/create/ticket',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'title':str,'description':str,'max_buy':int,'min_buy':int,'paid':bool,'status':bool})
def create_ticket():
    data = request.get_json()
    ticket:Tickets =TicketSchema().load(data)
    ticket.save()

    ticketData = TicketSchema().dump(ticket)
    return jsonify({'status':200,'message':'ticket created successfully','data':ticketData,'success':True}),200




@app.route('/api/v1/get/tickets',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_tickets():

    tickets:Tickets = Tickets.query.all()
    tickets = TicketSchema(many=True).dump(tickets)

    return  jsonify({'status':200,'message':'success','data':tickets,'success':True}),200
    
@app.route('/api/v1/get/ticket/<int:id_ticket>',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_ticket(id_ticket):

    ticket:Tickets = Tickets.query.get(id_ticket)
    ticket = TicketSchema().dump(ticket)

    return  jsonify({'status':200,'message':'success','data':ticket,'success':True}),200