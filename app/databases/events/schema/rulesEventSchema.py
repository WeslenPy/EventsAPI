from app.server.instance import app

from app.databases.events.models import RulesEvent,Users,Events

from marshmallow import pre_load,post_load,fields,validates_schema
from app.utils.functions.validitys import validity_field

class RulesEventSchema(app.ma.SQLAlchemyAutoSchema):

        
    @validates_schema
    def validates_fields(self,data:dict,**kwargs):
        event_id = data.get('event_id',None)
        user_id = data.get('user_id',None)

        validity_field.find_field_model(Users,{'id':user_id,"active":True},'user_id')
        validity_field.find_field_model(Events,{'id':event_id,'user_id':user_id,"status":True},'event_id')

        return data


    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data

    class Meta:
        unknown = "exclude"
        ordered = True
        model = RulesEvent
        load_instance = True
        dump_only = ("id",)
