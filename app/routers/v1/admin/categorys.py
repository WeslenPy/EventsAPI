from app.databases.events.schema import CategorySchema,category_model
from flask_restx import Resource,Api
from marshmallow import ValidationError
from app.server import app

api:Api = app.admin_api

@api.route("/create/category")
class Category(Resource):
    
    @api.expect(category_model,validate=True)
    @api.doc("Rota para cadastrar categorias")
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

# @v1.route('create/category',methods=['POST'])
# @decorators.authUserDecorator()
# @decorators.validityDecorator({'name':str,'description':str,'status':bool})
# def create_category():
#     data = request.get_json()
    
#     categoryFind =Category.query.filter_by(name=data['name']).first()
#     if not categoryFind:
#         new_category:Category = CategorySchema().load(data)
#         new_category.save()

#         categoryData = CategorySchema().dump(new_category)
#         return jsonify({'status':200,'message':'category created successfully','data':categoryData,'success':True}),200
    
#     categoryData = CategorySchema().dump(categoryFind)
#     return jsonify({'status':200,'message':'category has already been registered','data':categoryData,'success':False}),200
    

# @v1.route('get/categorys',methods=['GET'])
# @decorators.authUserDecorator()
# def get_categorys():

#     categorys:Category = Category.query.all()
#     categorys = CategorySchema(many=True).dump(categorys)

#     return  jsonify({'status':200,'message':'success','data':categorys,'success':True}),200

# @v1.route('get/category/<int:id_category>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_category(id_category):

#     category:Category = Category.query.get(id_category)
#     category = CategorySchema().dump(category)

#     return  jsonify({'status':200,'message':'success','data':category,'success':True}),200
