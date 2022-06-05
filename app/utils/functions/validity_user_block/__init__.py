from app.utils.message.userMessages import block 
from app.models import BlockingRule
from flask import jsonify
from time import time

def validityBlockUser(user):
    if user and not user.blocked_time is None and float(user.blocked_time) >= time():
        minutes_block = BlockingRule.query.first().blocking_time_minutes
        return jsonify({'data':{},
                        'message':block.format(minutes_block=minutes_block),
                        'error':1,'status':False}),200

    if user.purchase_progress:
        return jsonify({'data':{},'message':'Você possui uma compra em andamento','error':1,'status':False}),200

    return False