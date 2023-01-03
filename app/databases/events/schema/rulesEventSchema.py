from app import ma
from app.databases.events.models import RulesEvent

class RulesEventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = RulesEvent
        load_instance = True
        dump_only = ("id",)
