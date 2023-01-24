from app.server.instance import app

from app.databases.events.models import RulesEvent
from marshmallow import post_load,validates

class RulesEventSchema(app.ma.SQLAlchemyAutoSchema):
    
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
