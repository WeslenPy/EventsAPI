from app.server.instance import app

from app.databases.events.models    import Events

from app.databases.events.schema.categorySchema import CategorySchema
from app.databases.events.schema.ticketSchema import TicketSchema
from app.databases.events.schema.userSchema import UserSchema
from app.databases.events.schema.partnerUserSchema import PartnerUserSchema
from app.databases.events.schema.rulesEventSchema import RulesEventSchema
from app.databases.events.schema.termsEventSchema import TermsEventSchema

from marshmallow import pre_load,post_load,fields



class DateTimeIso(fields.Field):
    def _serialize(self, value, attr, obj,**kwargs):
        print(value,attr,obj)
        if value is None:return None
        return obj.datetime_isoformat(value)

class EventSchema(app.ma.SQLAlchemyAutoSchema):
    
    event_partner_children = app.ma.Nested(PartnerUserSchema,many=True)
    terms_children = app.ma.Nested(TermsEventSchema,many=True)
    rules_event_children = app.ma.Nested(RulesEventSchema,many=True)
    ticket_ship = app.ma.Nested(TicketSchema)
    category_ship = app.ma.Nested(CategorySchema)
    user_ship = app.ma.Nested(UserSchema)

    image = app.ma.String(required=True)
    video = app.ma.String(required=True)

    start_date = DateTimeIso(required=True)
    start_hour = DateTimeIso(required=True)
    end_date = DateTimeIso(required=True)

    @pre_load
    def upload_files(self,data,**kwargs):
        pass
        return data

    @post_load(pass_original=True)
    def _new(self,data,original_data,**kwargs):
        Events(**original_data).save()
        return data


    class Meta:
        model = Events
        ordered = True
        include_fk=True
        load_instance = True
        # unknown = "exclude"
        dump_only = ("id",)

