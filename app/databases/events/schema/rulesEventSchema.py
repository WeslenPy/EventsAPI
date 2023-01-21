from app.server.instance import app

from app.databases.events.models import RulesEvent

class RulesEventSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = RulesEvent
        load_instance = True
        dump_only = ("id",)
