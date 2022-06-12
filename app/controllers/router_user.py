from flask import render_template,request,jsonify,session
from flask_mail import Message

from sqlalchemy.sql import functions

from app.utils.functions import decorators,not_found,validity_cpf
from app import app,db,tokenSafe,executor,mail
from app.api import NumberAPI
from app.models import *
from app.schema import *


@app.route('/register',methods=['POST'])
@decorators.validityDecorator({'first_name':str,'last_name':str,'email':str,'password':str})
def register():

    data = request.json

    first_name = str(data['first_name']).strip()
    last_name = str(data['last_name']).strip()
    email = str(data['email']).strip()
    password = str(data['password']).strip()

    if Users.query.filter_by(email=email).first():
        return jsonify({'message':'Email já foi cadastrado.','error':1}),200

    user = Users(first_name=first_name,last_name=last_name,password=password,
                email=email)

    db.session.add(user)
    db.session.commit()

    token_url = tokenSafe.dumps(email,salt='emailConfirmUser')
    msg = Message("Não responda este e-mail",
            sender="noreply@meunumerovirtual.com",
            recipients=[email])

    url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
    msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=first_name))
    executor.submit(mail.send,msg)
    
    session['admin_logger'] = [False,False]

    return jsonify({
            'status':200,
            'message':'Enviamos um link de confirmação para seu e-mail, acesse-o para ativar sua conta!',
            'error':0}),200



