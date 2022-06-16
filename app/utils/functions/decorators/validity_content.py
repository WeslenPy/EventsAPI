from flask import request,jsonify
from functools import wraps


def validityDecorator(data):
    def returnDecorator(func):
        @wraps(func)
        def wrapper(*args):
            typeData = type(data)
            message = jsonify({'message':'missing or invalid field','arg':'','success':False}),200

            for item in data:
                current = request.json.get(item,'NOTCONTENT')

                if current=='NOTCONTENT' or not current:return message
                elif typeData == dict:
                    if type(data[item]) in [list,tuple]:
                        if type(current) not in data[item]:
                            message['arg'] = item
                            return message
                    else:
                        if type(current) != data[item]:
                            message['arg'] = item
                            return message

            return func(*args)
            
        return wrapper
        
    return returnDecorator