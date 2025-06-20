from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from app.utils.messages import not_autorization
from functools import wraps
from flask_restx import Api
from flask import request

def authType(required:bool=False,
            type:list[str]=['user'],
            location:str='json',api:Api=None):

    def returnDecorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:verify_jwt_in_request()
            except:return not_autorization,401
            
            user = get_jwt_identity()
            if required:
                if location == 'json':api.payload['user_id'] = user
                elif location == "form":request.form['user_id']=user
                elif location == "params":kwargs['user_id']=user
                
            return func(*args,**kwargs)

        return wrapper
        
    return returnDecorator  