
from app.utils.functions import decorators
from flask import request,jsonify

from app.databases.events.models import TermsEvent,Events
from app.databases.events.schema import TermsEventSchema

from app.blueprints import v1

"""
POST REGISTER DATA 
"""

@v1.route('create/term',methods=['POST'])
@decorators.authUserDecorator(required=True)
@decorators.validityDecoratorForm(['type_term','description',"event_id","user_id"])
def create_term():
    data = request.get_json()

    eventFind:Events =Events.query.filter_by(status=True,id=data['event_id'],user_id=data['user_id']).first()
    if not eventFind:
        return jsonify({'status':400,'message':'Invalid event','success':False}),200


    new:TermsEvent = TermsEventSchema().load(data)
    new.save()

    term = TermsEventSchema().dump(new)

    return jsonify({'status':200,'message':'term created successfully',"data":term,'success':False}),200
    

@v1.route('get/terms',methods=['GET'])
@decorators.authUserDecorator(param=True)
def get_terms(currentUser):

    terms:TermsEvent = TermsEvent.query.filter_by(user_id=currentUser).all()
    terms = TermsEventSchema(many=True).dump(terms)
    return  jsonify({'status':200,'message':'success','data':terms,'success':True}),200

@v1.route('get/term/<int:id_term>',methods=['GET'])
@decorators.authUserDecorator(param=True)
def get_term(id_term,currentUser):

    term:TermsEvent = TermsEvent.query.filter_by(user_id=currentUser,id=id_term).first()
    term = TermsEventSchema().dump(term)

    return  jsonify({'status':200,'message':'success','data':term,'success':True}),200

