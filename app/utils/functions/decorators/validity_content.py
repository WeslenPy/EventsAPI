from flask import request,jsonify
from functools import wraps


def validityDecorator(data):
    def returnDecorator(func):
        @wraps(func)
        def wrapper(*args):
            typeData = type(data)
            message = jsonify({'message':'Revise os dados e tente novamente!','error':1}),200

            for item in data:
                current = request.json.get(item,None)

                if current==None or not current:return message
                elif typeData == dict:
                    if type(data[item]) in [list,tuple]:
                        if type(current) not in data[item]:
                            return message
                    else:
                        if type(current) != data[item]:
                            return message

            return func(*args)
            
        return wrapper
        
    return returnDecorator