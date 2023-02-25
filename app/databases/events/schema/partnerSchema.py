from app.server.instance import app
from app.databases.events.models    import Partner,Users,Events

from app.databases.events.schema .eventSchema import EventSchema
from app.databases.events.schema .userSchema import UserSchema

from app.utils.functions.validitys import validity_field
from marshmallow import validates_schema,post_load

class PartnerSchema(app.ma.SQLAlchemyAutoSchema):
    
    event_ship = app.ma.Nested(EventSchema)
    user_ship = app.ma.Nested(UserSchema)


    @post_load
    def new_partner(self,data,**kwargs):
        data.save()
        return data

    @validates_schema
    def check_ids(self,data,**kwargs):
        user_id = data.get('user_id',None)
        event_id = data.get('event_id',None)

        validity_field.find_field_model(Users,{'id':user_id,"active":True},'user_id')
        validity_field.find_field_model(Events,{'id':event_id,'status':True},'event_id')

    class Meta:
        model = Partner
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

