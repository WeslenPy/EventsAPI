from app import ma
from app.databases.events.models import UserAccessTypes
from app.databases.events.schema.userTypesSchema import UserTypesSchema


class UserAccessTypesSchema(ma.SQLAlchemyAutoSchema):

    type_ship = ma.Nested(UserTypesSchema)
    
    class Meta:
        unknown = "exclude"
        model = UserAccessTypes

        load_instance = True
        include_fk=True
        ordered = True

        dump_only = ("id",)