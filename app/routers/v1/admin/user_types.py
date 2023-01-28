
from app.databases.events.schema  import UserTypesSchema,user_types_model
from app.databases.events.models import UserTypes
from app.utils.functions.decorators import auth
from flask_restx import Resource,Api
from marshmallow import ValidationError
from app.server import app


api:Api = app.admin_api

@api.route("/create/user/type")
class UserTypeRouter(Resource):
    
    @api.expect(user_types_model,validate=True)
    @api.doc("Rota para cadastrar tipos de acesso")
    @auth.authType()
    def post(self,**kwargs):
        data = api.payload
        _schema =  UserTypesSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'status':200,
            'message':'User type created successfully',
            'error':False},200


@api.route("/user/types/all")
class Genre(Resource):
    
    @api.doc("Lista de tipos de usuario",security=None)
    @api.marshal_list_with(user_types_model)
    def get(self):

        data:list[UserTypes] = UserTypes.query.filter_by(status=True).all()
        _schema:UserTypesSchema =  UserTypesSchema(many=True)
        data= _schema.dump(data)

        return data,200
