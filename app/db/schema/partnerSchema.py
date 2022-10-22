from app import ma
from app.db.models  import Partner

from app.db.schema .eventSchema import EventSchema
from app.db.schema .userSchema import UserSchema


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

