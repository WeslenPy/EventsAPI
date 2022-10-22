from flask import request,jsonify
from functools import wraps
from datetime import datetime
import sys

def validityDecorator(data):
    def returnDecorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):

            typeData = type(data)
            message = {'status':400,'message':'missing or invalid field','json_error':False,'details':{'param':'','invalid_type':False,'invalid_param':False},'success':False}

            try:
                json_data= request.get_json()
            except:
                message['json_error'] = True
                return  jsonify(message),400

            for check in json_data:
                if check not in data:
                    message['details']['param'] = check
                    message['details']['invalid_param'] = True

                    return  jsonify(message),400

            for item in data:

                current = json_data.get(item,None)

                if current is None or not current:
                    message['details']['param'] = item
                    return  jsonify(message),400

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

            return func(*args,**kwargs)
            
        return wrapper
        
    return returnDecorator


def validityDecoratorForm(data):
    def returnForm(func):
        @wraps(func)
        def wrapper(*args,**kwargs):

            print(request.form,file=sys.stderr)

            message = {'status':400,'message':'missing or invalid field','form_error':False,
                                'details':{'param':'','invalid_type':False,'invalid_param':False},'success':False}

            try:
                json_data = {}
                form_data = request.form
                files = request.files
                
                for file in files:json_data[file]=files[file]
                for params in form_data:json_data[params]=form_data[params]
                json_data['user_id'] = kwargs['currentUser']

            except:
                message['form_error'] = True
                return  jsonify(message),400


            for check in json_data:
                if check not in data:
                    message['details']['param'] = check
                    message['details']['invalid_param'] = True

                    return  jsonify(message),400

            for item in data:

                current = json_data.get(item,None)

                if current is None or not current:
                    message['details']['param'] = item
                    return  jsonify(message),400

            kwargs['data'] = json_data
            return func(*args,**kwargs)
        return wrapper
    return returnForm

def pattern_message(item,message):
    message['details']['param'] = item
    message['details']['invalid_type'] = True
    return  jsonify(message),400


def convertToDatetime(date):
    try:
        new = datetime.strptime(date, "%Y-%m-%d").isoformat()
        return new
    except:
        return False