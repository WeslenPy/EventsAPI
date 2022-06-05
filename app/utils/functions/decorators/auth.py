from flask import request,jsonify
from functools import wraps
from app import jwtGen


def authUserDecorator(required=False):
    def returnDecorator(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            if 'Authorization' not in request.headers:
                return jsonify({'message':'Access denied','error':401}),401

            token= request.headers['Authorization']
            token = jwtGen.token_required(token)
            if token[1] !=200: return token

            if required:kwargs['currentUser'] = token[-1]
            return func(*args,**kwargs)

        return wrapper
        
    return returnDecorator