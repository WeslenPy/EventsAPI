from app import ma
from app.models import Partner
from dataclasses import dataclass
from app.schema.eventSchema import EventSchema
from app.schema.userSchema import UserSchema

@dataclass
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

