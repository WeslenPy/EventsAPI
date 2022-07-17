from app import ma
from app.models import Lots,Tickets

class LotSchema(ma.SQLAlchemyAutoSchema):
    ticket_ship = ma.Nested(Tickets)
    
    class Meta:
        model = Lots
        unknown = "exclude"
        ordered = True
        load_instance = True
        dump_only = ("id",)