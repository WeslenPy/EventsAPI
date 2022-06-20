from app import ma
from app.models import Tickets

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = Tickets
        load_instance = True
        dump_only = ("id",)

