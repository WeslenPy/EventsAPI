from app.server.instance import app

from app.databases.events.models    import Partner
from app.databases.events.schema .userSchema import UserSchema
from marshmallow import post_load

class PartnerUserSchema(app.ma.SQLAlchemyAutoSchema):

    user_ship = app.ma.Nested(UserSchema)

    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data

    class Meta:
        model = Partner
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)

