from app.server.instance import app

from app.databases.events.models    import UserTypes


class UserTypesSchema(app.ma.SQLAlchemyAutoSchema):
    
    class Meta:
        unknown = "exclude"
        model = UserTypes

        load_instance = True
        include_fk=True
        ordered = True

        dump_only = ("id",)