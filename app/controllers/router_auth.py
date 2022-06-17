from flask import request,jsonify
from app.utils.functions import validitys,decorators
from app.models import Users
from app import app,jwtGen



@app.route('/api/v1/login',methods=['POST'])
@decorators.validityDecorator({"email":str,"password":str})
def login_user():
    data = request.json
    email = data.get('email',None)
    password = data.get('password',None)

    user = Users.query.filter_by(email=email).first()

    if user:
        if validitys.comparePassword(password,user.password):
            # if not user.active:return jsonify({'message':'Activate your account to proceed with login.','success':False,'status':401}),401
        
            token = jwtGen.get_token(user.id,email)

            return jsonify({'message':'login successfully','success':True,'token':token,"status":200}),200

    return jsonify({'message':'Invalid email or password(s)!','success':False,"status":401}),401
        

