from app.server.instance import app

from app.databases.events.models import UserAccessTypes
from app.databases.events.schema.userTypesSchema import UserTypesSchema


class UserAccessTypesSchema(app.ma.SQLAlchemyAutoSchema):

    type_ship = app.ma.Nested(UserTypesSchema)

    
    
    class Meta:
        unknown = "exclude"
        model = UserAccessTypes

        load_instance = True
        include_fk=True
        ordered = True

        dump_only = ("id",)