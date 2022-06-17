from app import ma
from app.models import GenreTypes

class GenreTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"

        model = GenreTypes
        load_instance = True
