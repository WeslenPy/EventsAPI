from app import ma
from app.models import Events

from app.schema.categorySchema import CategorySchema
from app.schema.ticketSchema import TicketSchema
from app.schema.userSchema import UserSchema
from app.schema.partnerSchema import PartnerSchema

class EventSchema(ma.SQLAlchemyAutoSchema):
    
    event_partner_children = ma.Nested(PartnerSchema,many=True)
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

