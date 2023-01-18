from app import ma
from app.databases.events.models    import UserTypes


class UserTypesSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        unknown = "exclude"
        model = UserTypes

        load_instance = True
        include_fk=True
        ordered = True

        dump_only = ("id",)