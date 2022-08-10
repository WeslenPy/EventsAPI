
from app.utils.functions import decorators
from flask import request,jsonify
from app import app

from app.models import Partner,Users,Events
from app.schema import PartnerSchema


"""
POST REGISTER DATA 
"""

@app.route('/api/v1/add/partner',methods=['POST'])
@decorators.authUserDecorator()
@decorators.validityDecorator({'user_id':int,'event_id':int,"status":bool})
def add_partner():
    data = request.get_json()

    if not Users.query.filter_by(id=data['user_id'],active=True):
        return jsonify({'status':400,'message':"Invalid user_id",'success':False}),400  
        
    elif not Events.query.filter_by(id=data['event_id'],status=True):
        return jsonify({'status':400,'message':"Invalid event_id or inactive event",'success':False}),400

    partnerFind =Partner.query.filter_by(user_id=data['user_id'],event_id=data['event_id']).first()
    if not partnerFind:
        partner:Partner = PartnerSchema().load(data)
        partner.save()

        partnerData = PartnerSchema().dump(partner)
        return jsonify({'status':200,'message':'partner created successfully','data':partnerData,'success':True}),200

    partnerData = PartnerSchema().dump(partnerFind)
    return jsonify({'status':200,'message':'partner has already been registered','data':partnerData,'success':False}),200
    
   