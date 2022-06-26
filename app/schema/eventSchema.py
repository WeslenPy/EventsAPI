from app.schema import CategorySchema,TicketSchema,UserSchema,PartnerSchema
from app.models import Events
from app import ma

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

