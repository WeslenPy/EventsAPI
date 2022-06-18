from app import ma
from app.models import Events,Tickets

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = Events
        load_instance = True

class TicketEventSchema(ma.SQLAlchemyAutoSchema):
    ticket = ma.Nested(Tickets)
    class Meta:
        unknown = "exclude"
        model = Events
        load_instance = True
        ordered = True
