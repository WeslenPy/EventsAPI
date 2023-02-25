from app.databases.events.models import Users
from flask_restx import Resource
from app.server import app

api_user = app.user_api

@api_user.route('/confirm/account/<string:token>')
class ConfirmAccountRouter(Resource):
    
    @api_user.doc("Rota para efetuar a confirmação do email.",security=None)
    def get(self,token):
        try:
            email = app.tokenSafe.loads(token,salt=app.app.config['TOKEN_SALT'],max_age=2000)
            user:Users  = Users.query.filter_by(email=email).first()
            if user: 
                if not user.active:
                    user.active = True
                    app.db.session.commit()
                
            return 200
        except:
            return 400