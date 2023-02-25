from app.server.instance import app

from app.databases.events.models    import Lots,Tickets
from marshmallow import post_load,validates_schema,validates
from app.utils.functions.validitys import validity_date,validity_field
class LotSchema(app.ma.SQLAlchemyAutoSchema):
    
    @post_load
    def new(self,data,**kwargs):
        data.save()
        return data

    @validates_schema
    def dates_check(self,data,**kwargs):
        start_date =  data.get('start_date')
        end_date =  data.get('end_date')
        validity_date.dateValidity(start_date,end_date)
        return data

    @validates('ticket_id')
    def exists_id(self,data,**kwargs):
        validity_field.find_field_model(Tickets,{'id':data},'ticket_id')
        return data

    
    class Meta:
        unknown = "exclude"
        model = Lots
        ordered = True
        include_fk=True
        load_instance = True
        dump_only = ("id",)