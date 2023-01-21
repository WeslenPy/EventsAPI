from app.server.instance import app

from app.databases.events.models import TermsEvent

class TermsEventSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = TermsEvent
        load_instance = True
        dump_only = ("id",)
