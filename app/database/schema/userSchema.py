from app import ma
from app.database.models    import Users

from app.database.schema .physicalPersonSchema import PhysicalPersonSchema
from app.database.schema .legalPersonSchema import LegalPersonSchema
from app.database.schema .genreTypesSchema import GenreTypeSchema

from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    
    physical_ship = ma.Nested(PhysicalPersonSchema)
    legal_ship = ma.Nested(LegalPersonSchema)
    genre_ship = ma.Nested(GenreTypeSchema)

    email = fields.Email()
    
    class Meta:
        unknown = "exclude"
        model = Users

        
        load_instance = True
        include_fk=True
        ordered = True

        load_only = ("password",)
        dump_only = ("id",)

