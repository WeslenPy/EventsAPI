from app.databases.events.schema import CategorySchema,category_model
from app.utils.functions.decorators import auth
from flask_restx import Resource,Api
from marshmallow import ValidationError
from app.server import app

api:Api = app.admin_api


@api.route("/create/category")
class Category(Resource):
    
    @api.expect(category_model,validate=True)
    @api.doc("Rota para cadastrar categorias")
    @auth.authType()
    def post(self,**kwargs):
        data = api.payload
        _schema =  CategorySchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201
        return {
            'status':200,
            'message':'Category created successfully',
            'error':False},200
