from app.utils.functions.validitys import validity_field
from app.databases.events.models import TermsEvent,Events,Users
from marshmallow import validates,pre_load,post_load
from app.server.instance import app

class TermsEventSchema(app.ma.SQLAlchemyAutoSchema):

    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data

    @validates('event_id')
    def exists_event_id(self,data,**kwargs):
        validity_field.find_field_model(Events,'id',data,'event_id')
        return data    
    
    @validates('user_id')
    def exists_user_id(self,data,**kwargs):
        validity_field.find_field_model(Users,'id',data,'user_id')
        return data
        
    class Meta:
        unknown = "exclude"
        ordered = True
        model = TermsEvent
        load_instance = True
        dump_only = ("id",)
