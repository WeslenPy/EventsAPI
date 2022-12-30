from app.utils.functions import validitys,decorators
from app.database.models import Users
from flask import request,jsonify
from app.blueprints import v1
from app import jwt


@v1.route('auth',methods=['POST'])
@decorators.validityDecorator({"email":str,"password":str})
def auth_user():
    data = request.json
    email = data.get('email',None)
    password = data.get('password',None)

    user:Users = Users.query.filter_by(email=email).first()

    if user:
        if validitys.comparePassword(password,user.password):
            # if not user.active:
                # return jsonify({'message':'Activate your account to proceed with login.',
                #                  'success':False,'status':401}),401
        
            token = jwt.generate(user.id)

            return jsonify({'message':'login successfully','success':True,'token':token,"status":200}),200

    return jsonify({'message':'Invalid email or password!','success':False,"status":401}),401
        
