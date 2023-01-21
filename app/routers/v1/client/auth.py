from flask_restx import Resource,Api,fields
from app.databases.events.models import Users
from app.utils.functions import validitys
from app.server import app

# payload = {}
api = app.api
auth_model =app.api.model('Auth', {
    "email":fields.String(required=True),
    "password":fields.String(required=True)
})

@app.api.route("/auth")
class Auth(Resource):
    
    @api.expect(auth_model)
    def post(self,**kwargs):
        data = api.payload
        user:Users = Users.query.filter_by(email=data.get('email','')).first()

        if user:
            if validitys.comparePassword(data.get('password',''),user.password):
                if not user.active:
                    return {'message':'Activate your account to proceed with login.',
                                     'success':False,'status':401},401
            
                return {'message':'login successfully','success':True,
                                'token': app.jwt.generate(user.id),"status":200},200

        return {'message':'Invalid email or password!','success':False,"status":401},401
        