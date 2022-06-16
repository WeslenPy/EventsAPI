from app import ma
from app.models import Tickets

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tickets
        load_instance = True
