from unicodedata import category
from app import ma
from app.models import Events,Tickets,Category

class EventSchema(ma.SQLAlchemyAutoSchema):
    ticket = ma.Nested(Tickets)
    category = ma.Nested(Category)
    class Meta:
        unknown = "exclude"
        ordered = True
        model = Events
        load_instance = True

