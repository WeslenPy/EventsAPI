from flask import request,jsonify
from functools import wraps


def validityDecorator(data):
    def returnDecorator(func):
        @wraps(func)
        def wrapper(*args):
            typeData = type(data)
            message = {'status':200,'message':'missing or invalid field','json_error':False,'details':{'param':'','invalid_type':False,'invalid_param':False},'success':False}

            try:json_data= request.get_json()
            except:
                message['json_error'] = True
                return  jsonify(message),200


            for check in json_data:
                if check not in data:
                    message['details']['param'] = check
                    message['details']['invalid_param'] = True

                    return  jsonify(message),200


            for item in data:

                current = json_data.get(item,'NOTCONTENT')

                if current=='NOTCONTENT' or not current:
                    message['details']['param'] = item
                    return  jsonify(message),200

                elif typeData == dict:
                    
                    if type(data[item]) in [list,tuple]:
                        if type(current) not in data[item]:
                            message['details']['param'] = item
                            message['details']['invalid_type'] = True
                            return jsonify(message),200
                    else:
                        if type(current) != data[item]:
                            message['details']['param'] = item
                            message['details']['invalid_type'] = True
                            return  jsonify(message),200

            return func(*args)
            
        return wrapper
        
    return returnDecorator