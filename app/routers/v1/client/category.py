from flask_restx import Resource,fields
from app.databases.events.schema import CategorySchema,category_model
from app.databases.events.models import Category
from app.utils.functions.decorators import auth
from app.server import app

api = app.category_api

categorys_model = api.clone("Categorys",app.default_model,{
    'data':fields.Nested(category_model,description="Todas as categorias cadastrados",as_list=True),
})


@api.route("/all",endpoint="Category")
class Categorys(Resource):
    
    @api.doc("Rota para pegar todas as categorias")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success",categorys_model)
    @auth.authType()
    def get(self,**kwargs):
        categorys = Category.query.filter_by(status=True).all()
        _data = CategorySchema(many=True).dump(categorys)

        return {'message':'Success',
                "data":_data,
                'error':False,
                "code":200},200
        