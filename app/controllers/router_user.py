from flask import render_template,request,jsonify
from app.utils.functions import decorators,validity_cpf
from app import app,db,tokenSafe,executor,mail
from flask_mail import Message
from datetime import datetime
from app.models import *
from app.schema import *


@app.route('/api/v1/register/physical',methods=['POST'])
@decorators.validityDecorator({'email':str,'password':str,'phone':str,'cep':int,'address':str,'number_address':int,'state':str,
                 'complement':str,'district':str,'city':str,'cpf':str,'full_name':str,'birth_day':[str,datetime],'genre_id':int})
def register_physical():

    data = request.json
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'status':200,
                        'message':'Email has already been registered.',
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


    physical = PhysicalPerson(data['full_name'],data['cpf'],data['birth_day'])
    db.session.add(physical)
    db.session.commit()

    new_user = Users(data['email'],data['password'],data['phone'],data['cep'],
                    data['address'],data['number_address'],data['complement'],data['district'],data['city'],data['state'],
                    physical_id=physical.id,genre_id=data['genre_id'])

    db.session.add(new_user)
    db.session.commit()

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

    new_juridical = LegalPerson(data['corporate_name'],data['cnpj'])
    db.session.add(new_juridical)
    db.session.commit()

    new_user = Users(data['email'],data['password'],data['phone'],data['cep'],data['address'],
                        data['number_address'],data['complement'],data['district'],data['city'],
                        legal_id=new_juridical.id)

    db.session.add(new_user)
    db.session.commit()

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



