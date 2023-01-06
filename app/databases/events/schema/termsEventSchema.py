from app import ma
from app.databases.events.models import TermsEvent

class TermsEventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = TermsEvent
        load_instance = True
        dump_only = ("id",)
