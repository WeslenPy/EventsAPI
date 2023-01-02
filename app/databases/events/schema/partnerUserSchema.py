from app import ma
from app.database.models    import Partner
from app.database.schema .userSchema import UserSchema


class PartnerUserSchema(ma.SQLAlchemyAutoSchema):

    user_ship = ma.Nested(UserSchema)

    class Meta:
        model = Partner
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

