from flask import request,jsonify
from functools import wraps
from app.databases.events.models import Users
from app import jwt

def authUserDecorator(required=False,is_admin=False,param=False):
    def returnDecorator(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            if 'Authorization' not in request.headers:
                return jsonify({'status':401,'message':'Access denied','success':False}),401

            token= request.headers.get('Authorization','')
            token = jwt.token_required(token)

            if token[1] !=200:return token

            user:Users = Users.query.get(token[-1]['some']['id'])

            if required:request.json['user_id']=user.id
            elif param: kwargs['currentUser'] = user
            return func(*args,**kwargs)

        return wrapper
        
    return returnDecorator