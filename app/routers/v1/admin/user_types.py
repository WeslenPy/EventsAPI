
from app.utils.functions import decorators
from flask import request,jsonify
from app import app

from app.databases.events.models    import UserTypes
from app.databases.events.schema  import UserTypesSchema

from app.blueprints import v1

"""
POST REGISTER DATA 
"""

@v1.route('create/type/user',methods=['POST'])
@decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'type':str,'description':str,"status":bool})
def create_type_user():
    data = request.get_json()

    find =UserTypes.query.filter(UserTypes.type==data['type']).first()
    if not find:
        new:UserTypes = UserTypesSchema().load(data)
        new.save()

        data = UserTypesSchema().dump(new)
        return jsonify({'status':200,'message':'type user created successfully','data':data,'success':True}),200

    data = UserTypesSchema().dump(find)
    return jsonify({'status':200,'message':'type user has already been registered','data':data,'success':False}),200
    

@v1.route('get/types',methods=['GET'])
def get_types():

    find:UserTypes = UserTypes.query.all()
    find = UserTypesSchema(many=True).dump(find)

    return  jsonify({'status':200,'message':'success','data':find,'success':True}),200

@v1.route('get/type/<int:id>',methods=['GET'])
@decorators.authUserDecorator()
def get_type(id):

    find:UserTypes = UserTypes.query.get(id)
    find = UserTypesSchema().dump(find)

    return  jsonify({'status':200,'message':'success','data':find,'success':True}),200

