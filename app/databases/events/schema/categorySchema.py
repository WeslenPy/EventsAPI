from app.server.instance import app
from app.databases.events.models    import Category
from app.utils.functions.validitys import validity_field
from marshmallow import validates,post_load

from flask_restx import fields

api = app.admin_api
category_model =api.model('Category',{
                            'name':fields.String(required=True,description="Nome da categoria"),
                            'description':fields.String(description="Descrição das categoria"),
                            'status':fields.Boolean(default=True,description="Status da categoria"),
                            'created_at':fields.DateTime(readonly=True,description="Data de criação da categoria"),
                            })
                            
class CategorySchema(app.ma.SQLAlchemyAutoSchema):


    @post_load
    def new_category(self,data,**kwargs):
        data.save()
        return data

    @validates('name')
    def unique(self,data,**kwargs):
        validity_field.unique(Category,{"name":data})
        return data

    class Meta:
        unknown = "exclude"
        model = Category
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
