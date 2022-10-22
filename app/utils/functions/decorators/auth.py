from flask import request,jsonify
from functools import wraps
from app.database.models    import Users
from app import jwtGen



def authUserDecorator(required=False,is_admin=False,param=False):
    def returnDecorator(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            if 'Authorization' not in request.headers:
                return jsonify({'status':401,'message':'Access denied','success':False}),401

            token= request.headers.get('Authorization','')
            token = jwtGen.token_required(token)

            if token[1] !=200:return token
            if is_admin:
                user= Users.query.get(token[-1]['some']['id'])
                if user and not user.is_admin: return jsonify({'status':401,'message':'Access denied','success':False}),401

            user_id = token[-1]['some']['id']
            if required:request.json['user_id']=user_id
            elif param: kwargs['currentUser'] = user_id
            return func(*args,**kwargs)

        return wrapper
        
    return returnDecorator