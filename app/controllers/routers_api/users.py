
from functools import partial
from app.utils.functions import decorators,validitys
from app import app,tokenSafe,executor
from flask import request,jsonify
from datetime import datetime

from app.models import Users,PhysicalPerson,LegalPerson
from app.schema import UserSchema,PhysicalPersonSchema,LegalPersonSchema

"""
POST REGISTER DATA 
"""


@app.route('/api/v1/register/physical',methods=['POST'])
@decorators.validityDecorator({'email':str,'password':str,'phone':int,'cep':int,'address':str,'number_address':int,'state':str,
                 'complement':str,'district':str,'city':str,'cpf':str,'full_name':str,'birth_date':datetime,'genre_id':int})
def register_physical():

    data = request.get_json()

    
    
    result = validitys.validityAlready(data,'cpf')
    if result:return result

    physical:PhysicalPerson = PhysicalPersonSchema().load(data)
    physical.save()

    data['physical_id'] = physical.id
    new_user:Users = UserSchema().load(data)
    new_user.save()

#     token_url = tokenSafe.dumps(data['email'],salt='emailConfirmUser')
#     msg = Message("Não responda este e-mail",
#             sender=app.config['MAIL_USERNAME'],
#             recipients=[data['email']])

#     url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
#     msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=data['full_name']))
#     executor.submit(mail.send,msg)
    
    return jsonify({
            'status':200,
            'message':'Link send to email',
            'success':True}),200



@app.route('/api/v1/register/juridical',methods=['POST'])
@decorators.validityDecorator({'email':str,'password':str,'phone':str,'cep':int,'address':str,'number_address':int,
                 'complement':str,'district':str,'city':str,'cnpj':str,"corporate_name":str,'state':str})
def register_legal():

    data =  request.get_json()
    result = validitys.validityAlready(data,'cnpj')
    if result:return result

    new_juridical:LegalPerson = LegalPersonSchema().load(data)
    new_juridical.save()

    data['legal_id'] = new_juridical.id
    new_user:Users = UserSchema().load(data)
    new_user.save()

    # token_url = tokenSafe.dumps(data['email'],salt='emailConfirmUser')
    # msg = Message("Não responda este e-mail",
    #         sender=app.config['MAIL_USERNAME'],
    #         recipients=[data['email']])

    # url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
    # msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=data['corporate_name']))
    # executor.submit(mail.send,msg)
    
    return jsonify({
            'status':200,
            'message':'Link send to your email',
            'success':True}),200

"""
CHANGE DATA TABLE
"""


@app.route('/api/v1/edit/user/physical/<int:id_user>',methods=['PUT'])
# @decorators.authUserDecorator(is_admin=True)
def edit_physical(id_user):

    data = request.get_json()
    if not data:
        return jsonify({
            'status':404,
            'message':'fields not found',
            'success':False}),200



    edit_user:Users = Users.query.get(id_user)
    if edit_user:
        edit_user.update(data)
        edit_user = UserSchema().dump(edit_user)

        return jsonify({
            'status':200,
            'message':'user update successfully',
            'data':edit_user,
            'success':True}),200


    return jsonify({
            'status':404,
            'message':'user not found',
            'success':False}),200

"""
GET API DATA ALL
"""

@app.route('/api/v1/get/users',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_users():

    users:Users = Users.query.all()
    users = UserSchema(many=True).dump(users)

    return  jsonify({'status':200,'message':'success','data':users,'success':True}),200
    
@app.route('/api/v1/get/user/<int:id_user>',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_user(id_user):

    user:Users = Users.query.get(id_user)
    user = UserSchema().dump(user)

    return  jsonify({'status':200,'message':'success','data':user,'success':True}),200