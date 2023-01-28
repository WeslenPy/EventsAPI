from flask_restx import fields

from app.server.instance import app
from app.databases.events.models    import UserTypes

from marshmallow import post_load,pre_load


api = app.admin_api

user_types_model =api.model('UserType',{
                        'id':fields.Integer(readonly=True,description="Id do tipo do user"),
                        'access_level':fields.Integer(readonly=True,description="Nivel de acesso do user"),
                        'type':fields.String(required=True,description="Tipo do user"),
                        'description':fields.String(description="Descrição do tipo"), 
                        'status':fields.Boolean(readonly=True,description="Status do tipo",default=True), 
                        'created_at':fields.DateTime(readonly=True,description="Data de criação"), 
                        })


class UserTypesSchema(app.ma.SQLAlchemyAutoSchema):
    
    @post_load(pass_original=True)
    def _new(self,data,original_data,**kwargs):
        UserTypes(**original_data).save()
        return data

    class Meta:
        unknown = "exclude"
        model = UserTypes

        load_instance = True
        include_fk=True
        ordered = True

        dump_only = ("id",)