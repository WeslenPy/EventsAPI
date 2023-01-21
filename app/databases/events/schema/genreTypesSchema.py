from app.server.instance import app

from app.databases.events.models    import GenreTypes

class GenreTypeSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = GenreTypes
        load_instance = True
        dump_only = ("id",)
