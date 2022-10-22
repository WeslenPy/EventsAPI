from app import ma
from app.database.models    import GenreTypes

class GenreTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = GenreTypes
        load_instance = True
        dump_only = ("id",)
