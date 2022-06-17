from flask import request,jsonify,render_template,abort
from flask_mail import Message

from app.utils.functions import encrypt_password,decorators,validitys
from app import app,db,tokenSafe,mail,executor
from app.models import *
import hashlib


@app.route('/change/password',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({"actualPassword":str,"newPassword":str})
def change_password(currentUser):

    data = request.json
    user = Users.query.filter_by(id=currentUser['some']['id']).first()
    if user:
        if validitys.comparePassword(data['actualPassword'],user.password):
            user.password =encrypt_password.encryptPassword(data['newPassword'])
            db.session.commit()
            return jsonify({'status':200,'message':'Senha alterada com sucesso','success':True}),200
        
        return jsonify({'status':200,'message':'Senha invalida','success':False}),200
    
    return jsonify({'status':404,'message':'Usuário não encontrado','success':False}),404
    

@app.route('/confirm/<token>',methods=['GET'])
def validity_email(token):
    try:
        email = tokenSafe.loads(token,salt='emailConfirmUser',max_age=2000)
        user  = Users.query.filter_by(email=email).first()
        if user: 
            if not user.active:
                user.active = True
                db.session.commit()
                
                msg = Message("Bem-vindo!",
                  sender="noreply@meunumerovirtual.com",
                  recipients=[email])
        return ''
    except:
        return abort(404)


@app.route('/forgot/password',methods=['POST'])
@decorators.authUserDecorator()
@decorators.validityDecorator({"email":str})
def forgot_password_reset():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    result = not_found.checkContent(user)
    if result !=False:return result
    
    token_url = tokenSafe.dumps(user.id,salt='passwordForgot')
    msg = Message("Não responda este e-mail",
                sender="noreply@meunumerovirtual.com",
                recipients=[user.email])
        
    msg.html = str(render_template('email_reset.html',url_reset=f"{request.url}/{token_url}",username=user.first_name))
    executor.submit(mail.send,msg)
    
    return jsonify({'data':{},'message':'E-mail para recuperação de senha enviado.','success':True}),200

@app.route('/forgot/password/<token>',methods=['POST'])
@decorators.validityDecorator({"password":str})
def forgot_password(token):
    try:
        id_user = tokenSafe.loads(token,salt='passwordForgot',max_age=1200)
        user  = User.query.get(id_user)

        data = request.json
        user.password = hashlib.sha256(str.encode(data['password'])).hexdigest()
        db.session.commit()

        return jsonify({'data':{},'message':'Senha atualizada com sucesso','success':True}),200
    except:
        return abort(404)
