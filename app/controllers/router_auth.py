from flask import request,jsonify,session
from app.utils.functions import validity_password,decorators
from app.utils.message import userMessages
from app.models import User
from app import app,jwtGen


@app.route('/logout',methods=['POST'])
def logout():
    session['user'] = [False,False]
    return jsonify({'data':{},'message':'Logout feito com sucesso','error':1}),200

@app.route('/auth',methods=['POST'])
@decorators.validityDecorator({"email":str,"password":str})
def auth_user():
    data = request.json
    email = data.get('email',None)
    password = data.get('password',None)

    user = User.query.filter_by(email=email).first()

    if user:
        if validity_password.comparePassword(password,user.password):
            if not user.active:return jsonify({'message':userMessages.notActiveAccount,'error':401}),401
        
            token = jwtGen.get_token(user.id,email,user.first_name,user.last_name,user.cpf)

            if user.is_admin:session['user'] = [token,True]
            else:session['user'] = [token,False]

            return jsonify({'message':'success','error':0,'jwt':token}),200

    return jsonify({'message':'Email ou senha invalido(s)!','error':401}),401
        

@app.route('/auth/validate',methods=['GET'])
@decorators.authUserDecorator(True)
def auth_validate(currentUser):
    return jsonify(data=currentUser,message='success',error=0),200