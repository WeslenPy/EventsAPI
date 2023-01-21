from app.server.instance import app

from app.databases.events.models    import Lots
from .ticketSchema import TicketSchema

class LotSchema(app.ma.SQLAlchemyAutoSchema):
    # ticket_ship = app.ma.Nested(TicketSchema)
    
    class Meta:
        unknown = "exclude"
        model = Lots
        ordered = True
        include_fk=True
        load_instance = True
        dump_only = ("id",)