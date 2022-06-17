from flask import request,jsonify
from functools import wraps
from datetime import datetime

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

                current = json_data.get(item,None)

                if current is None or not current:
                    message['details']['param'] = item
                    return  jsonify(message),200

                elif typeData == dict:
                    
                    if type(data[item]) in [list,tuple]:
                        if data[item] == datetime:
                            new = convertToDatetime(current)
                            if  new:json_data[item] = new
                            else:return pattern_message(item,message)

                        elif type(current) not in data[item]:
                            return pattern_message(item,message)

                    else:
                        if data[item] == datetime:
                            new = convertToDatetime(current)
                            if new:json_data[item] = new
                            else:return pattern_message(item,message)

                        elif type(current) != data[item]:
                           return pattern_message(item,message)

            return func(*args)
            
        return wrapper
        
    return returnDecorator


def pattern_message(item,message):
    message['details']['param'] = item
    message['details']['invalid_type'] = True
    return  jsonify(message),200


def convertToDatetime(date):
    try:
        new = datetime.strptime(date, "%Y-%m-%d").isoformat()
        return new
    except:
        return False