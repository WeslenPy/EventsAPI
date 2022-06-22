from app import ma
from app.models import Events
from .categorySchema import CategorySchema
from .ticketSchema import TicketSchema
from .userSchema import UserSchema

class EventSchema(ma.SQLAlchemyAutoSchema):
    
    ticket_ship = ma.Nested(TicketSchema)
    category_ship = ma.Nested(CategorySchema)
    user_ship = ma.Nested(UserSchema)

    class Meta:
        model = Events
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

