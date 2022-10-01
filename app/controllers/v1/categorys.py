
from app.utils.functions import decorators
from flask import request,jsonify
from app import app

from app.schema import CategorySchema
from app.models import Category

"""
POST REGISTER DATA 
"""


@app.route('/api/v1/create/category',methods=['POST'])
@decorators.authUserDecorator()
@decorators.validityDecorator({'name':str,'description':str,'status':bool})
def create_category():
    data = request.get_json()
    
    categoryFind =Category.query.filter_by(name=data['name']).first()
    if not categoryFind:
        new_category:Category = CategorySchema().load(data)
        new_category.save()

        categoryData = CategorySchema().dump(new_category)
        return jsonify({'status':200,'message':'category created successfully','data':categoryData,'success':True}),200
    
    categoryData = CategorySchema().dump(categoryFind)
    return jsonify({'status':200,'message':'category has already been registered','data':categoryData,'success':False}),200
    

@app.route('/api/v1/get/categorys',methods=['GET'])
@decorators.authUserDecorator()
def get_categorys():

    categorys:Category = Category.query.all()
    categorys = CategorySchema(many=True).dump(categorys)

    return  jsonify({'status':200,'message':'success','data':categorys,'success':True}),200

@app.route('/api/v1/get/category/<int:id_category>',methods=['GET'])
@decorators.authUserDecorator()
def get_category(id_category):

    category:Category = Category.query.get(id_category)
    category = CategorySchema().dump(category)

    return  jsonify({'status':200,'message':'success','data':category,'success':True}),200
