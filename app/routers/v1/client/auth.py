from flask_restx import Resource,fields
from app.databases.events.models import Users
from app.utils.functions import validitys
from app.server import app


api_auth = app.user_api

auth_model =api_auth.model('Auth', {
    "email":fields.String(description='Email cadastrado.',required=True),
    "password":fields.String(description="Senha cadastrada.",required=True)
})

@api_auth.route("/auth",endpoint="Auth")
class Auth(Resource):
    
    @api_auth.expect(auth_model, validate=True)
    @api_auth.doc("Rota para efetuar a autenticação do usuario.",security=None)
    def post(self,**kwargs):
        data = api_auth.payload
        user:Users = Users.query.filter_by(email=data.get('email','')).first()

        if user:
            if validitys.comparePassword(data.get('password',''),user.password):
                if not user.active:
                    return {'message':'Activate your account to proceed with login.',
                                     'success':False,'status':401},401
            
                return {'message':'login successfully','success':True,
                                'token': app.jwt.generate(user.id),"status":200},200

        return {'message':'Invalid email or password!','success':False,"status":401},401
        