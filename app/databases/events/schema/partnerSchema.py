from app.server.instance import app

from app.databases.events.models    import Partner,Users,Events
from app.databases.events.schema .userSchema import UserSchema

from marshmallow import pre_load,post_load,fields,validates_schema
from app.utils.functions.validitys import validity_field
class PartnerSchema(app.ma.SQLAlchemyAutoSchema):

    user_ship = app.ma.Nested(UserSchema)
    
    @validates_schema
    def validates_fields(self,data:dict,**kwargs):
        event_id = data.get('event_id',None)
        user_id = data.get('user_id',None)

        validity_field.find_field_model(Users,{'id':user_id,"active":True},'user_id')
        validity_field.find_field_model(Events,{'id':event_id,"status":True},'event_id')

        return data



    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data

    class Meta:
        model = Partner
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

