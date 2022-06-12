from flask import request,jsonify,session
from app.utils.functions import validity_password,decorators
from app.models import Users
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

    user = Users.query.filter_by(email=email).first()

    if user:
        if validity_password.comparePassword(password,user.password):
            if not user.active:return jsonify({'message':'Ative sua conta para prosseguir com o login.','error':401}),401
        
            token = jwtGen.get_token(user.id,email)

            return jsonify({'message':'success','error':0,'jwt':token}),200

    return jsonify({'message':'Email ou senha invalido(s)!','error':401}),401
        

@app.route('/auth/validate',methods=['GET'])
@decorators.authUserDecorator(True)
def auth_validate(currentUser):
    return jsonify(data=currentUser,message='success',error=0),200