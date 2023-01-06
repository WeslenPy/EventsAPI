
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

    eventFind:Events =Events.query.filter_by(status=True,id=data['event_id'],
                                             user_id=data['user_id']).first()
    if not eventFind:
        return jsonify({'status':400,'message':'Invalid event','success':False}),200


    new:TermsEvent = TermsEventSchema().load(data)
    new.save()

    term = TermsEventSchema().dump(new)

    return jsonify({'status':200,'message':'term created successfully',"data":term,'success':False}),200
    


