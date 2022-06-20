from app import ma
from app.models import Users
from .physicalPersonSchema import PhysicalPersonSchema
from .legalPersonSchema import LegalPersonSchema
from .genreTypesSchema import GenreTypeSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    
    physical_ship = ma.Nested(PhysicalPersonSchema)
    legal_ship = ma.Nested(LegalPersonSchema)
    genre_ship = ma.Nested(GenreTypeSchema)
    
    class Meta:
        unknown = "exclude"
        model = Users
        
        load_instance = True
        include_fk=True
        ordered = True

        load_only = ("password",)
        dump_only = ("id",)

