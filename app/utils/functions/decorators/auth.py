from functools import wraps
from flask_jwt_extended import get_jwt_identity

def authType(type:list[str]=['user']):
    def returnDecorator(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            current_user = get_jwt_identity()
            return func(*args,**kwargs)

        return wrapper
        
    return returnDecorator  