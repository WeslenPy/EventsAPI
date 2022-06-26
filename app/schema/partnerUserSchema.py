from app import ma
from app.models import Partner
from app.schema.userSchema import UserSchema


class PartnerUserSchema(ma.SQLAlchemyAutoSchema):

    user_ship = ma.Nested(UserSchema)

    class Meta:
        model = Partner
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

