from app import ma
from app.databases.events.models    import Events

from app.databases.events.schema .categorySchema import CategorySchema
from app.databases.events.schema .ticketSchema import TicketSchema
from app.databases.events.schema .userSchema import UserSchema
from app.databases.events.schema .partnerUserSchema import PartnerUserSchema

class EventSchema(ma.SQLAlchemyAutoSchema):
    
    event_partner_children = ma.Nested(PartnerUserSchema,many=True)
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

