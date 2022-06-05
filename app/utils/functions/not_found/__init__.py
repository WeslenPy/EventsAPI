from flask import jsonify


def checkContent(data,message='Nenhum registro encontrado'):
    if data is None or not data:
        return  jsonify({'message':message,'error':1,'status':False}),404
    return False
