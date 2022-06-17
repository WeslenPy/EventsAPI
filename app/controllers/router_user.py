from flask import render_template,request,jsonify
from app.utils.functions import decorators,validity_cpf
from app import app,db,tokenSafe,executor,mail
from flask_mail import Message
from datetime import datetime
from app.models import *
from app.schema import *


@app.route('/api/v1/register/physical',methods=['POST'])
@decorators.validityDecorator({'email':str,'password':str,'phone':int,'cep':int,'address':str,'number_address':int,'state':str,
                 'complement':str,'district':str,'city':str,'cpf':str,'full_name':str,'birth_date':datetime,'genre_id':int})
def register_physical():

    data = request.get_json()
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'status':200,
                        'message':'Email has already been registered.',
                        'success':False}),200 
    
    elif Users.query.filter_by(phone=data['phone']).first():
        return jsonify({'status':200,
                        'message':'Phone has already been registered.',
                        'success':False}),200

    cpf =  validity_cpf.validatyCPF(data['cpf'])
    if not cpf:
        return ({'status':200,
                'message':'CPF is invalid.',
                'success':False}),200

    elif PhysicalPerson.query.filter_by(cpf=cpf).first():
        return ({'status':200,
                'message':'CPF has already been registered.',
                'success':False}),200

    data['cpf'] = cpf

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

    data = request.json
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'status':200,
                        'message':'Email has already been registered.',
                        'success':False}),200

    elif LegalPerson.query.filter_by(cnpj=data['cnpj']).first():
        return ({'status':200,
                'message':'CNPJ has already been registered.',
                'success':False}),200

    new_juridical = LegalPersonSchema().load(data)
    new_juridical.save()

    data['legal_id'] = new_juridical.id
    new_user = UserSchema().load(data)
    new_user.save()

    token_url = tokenSafe.dumps(data['email'],salt='emailConfirmUser')
    msg = Message("Não responda este e-mail",
            sender=app.config['MAIL_USERNAME'],
            recipients=[data['email']])

    url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
    msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=data['corporate_name']))
    executor.submit(mail.send,msg)
    
    return jsonify({
            'status':200,
            'message':'Link send to your email',
            'success':True}),200



