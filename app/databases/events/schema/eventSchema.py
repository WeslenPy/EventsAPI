from app.server.instance import app

from app.databases.events.models    import Events

from app.databases.events.schema.categorySchema import CategorySchema
from app.databases.events.schema.ticketSchema import TicketSchema
from app.databases.events.schema.userSchema import UserSchema
from app.databases.events.schema.partnerUserSchema import PartnerUserSchema
from app.databases.events.schema.rulesEventSchema import RulesEventSchema
from app.databases.events.schema.termsEventSchema import TermsEventSchema

from marshmallow import post_load


def make_url(obj):
    print(obj)
    return obj

class EventSchema(app.ma.SQLAlchemyAutoSchema):
    
    event_partner_children = app.ma.Nested(PartnerUserSchema,many=True)
    terms_children = app.ma.Nested(TermsEventSchema,many=True)
    rules_event_children = app.ma.Nested(RulesEventSchema,many=True)
    ticket_ship = app.ma.Nested(TicketSchema)
    category_ship = app.ma.Nested(CategorySchema)
    user_ship = app.ma.Nested(UserSchema)

    image = app.ma.Function(serialize=make_url)
    video = app.ma.Function(serialize=make_url)

    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data


    class Meta:
        model = Events
        ordered = True
        include_fk=True
        load_instance = True
        # unknown = "exclude"
        dump_only = ("id",)

