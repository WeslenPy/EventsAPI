from app import ma
from app.databases.events.models    import Partner

from app.databases.events.schema .eventSchema import EventSchema
from app.databases.events.schema .userSchema import UserSchema


class PartnerSchema(ma.SQLAlchemyAutoSchema):
    
    event_ship = ma.Nested(EventSchema)
    user_ship = ma.Nested(UserSchema)

    class Meta:
        model = Partner
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

