from app.server.instance import app

from app.databases.events.models import UserAccessTypes,Users,UserTypes
from app.databases.events.schema.userTypesSchema import UserTypesSchema

from marshmallow import pre_load,post_load,fields,validates_schema
from app.utils.functions.validitys import validity_field

class UserAccessTypesSchema(app.ma.SQLAlchemyAutoSchema):

    type_ship = app.ma.Nested(UserTypesSchema)
           
    @validates_schema
    def validates_fields(self,data:dict,**kwargs):
        type_id = data.get('type_id',None)
        user_id = data.get('user_id',None)

        validity_field.find_field_model(Users,{'id':user_id,"active":True},'user_id')
        validity_field.find_field_model(UserTypes,{'id':type_id,"status":True},'type_id')

        return data

    class Meta:
        unknown = "exclude"
        model = UserAccessTypes

        load_instance = True
        include_fk=True
        ordered = True

        dump_only = ("id",)