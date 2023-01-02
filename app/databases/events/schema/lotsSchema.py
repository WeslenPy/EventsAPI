from app import ma
from app.databases.events.models    import Lots
from .ticketSchema import TicketSchema

class LotSchema(ma.SQLAlchemyAutoSchema):
    # ticket_ship = ma.Nested(TicketSchema)
    
    class Meta:
        unknown = "exclude"
        model = Lots
        ordered = True
        include_fk=True
        load_instance = True
        dump_only = ("id",)