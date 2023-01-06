
from app.utils.functions import decorators
from flask import request,jsonify

from app.databases.events.models    import RulesEvent
from app.databases.events.schema  import RulesEventSchema

from app.blueprints import v1

"""
POST REGISTER DATA 
"""

@v1.route('create/rule',methods=['POST'])
@decorators.authUserDecorator(required=True)
@decorators.validityDecorator({'type':str,'description':str,"event_id":int,"user_id":int,"status":bool})
def create_rule():
    data = request.get_json()

    findRule =RulesEvent.query.filter(RulesEvent.type==data['type'],
                                      RulesEvent.event_id==data['event_id'],
                                      RulesEvent.user_id==data['user_id']).first()
    if not findRule:
        rule:RulesEvent = RulesEventSchema().load(data)
        rule.save()

        ruleData = RulesEventSchema().dump(rule)
        return jsonify({'status':200,'message':'rule created successfully','data':ruleData,'success':True}),200

    ruleData = RulesEventSchema().dump(findRule)
    return jsonify({'status':200,'message':'rule has already been registered','data':ruleData,'success':False}),200
    

@v1.route('get/rules',methods=['GET'])
def get_rules():

    rules:RulesEvent = RulesEvent.query.all()
    rules = RulesEventSchema(many=True).dump(rules)

    return  jsonify({'status':200,'message':'success','data':rules,'success':True}),200

@v1.route('get/rule/<int:id_rule>',methods=['GET'])
@decorators.authUserDecorator()
def get_rule(id_rule):

    rule:RulesEvent = RulesEvent.query.get(id_rule)
    rule = RulesEventSchema().dump(rule)

    return  jsonify({'status':200,'message':'success','data':rule,'success':True}),200

