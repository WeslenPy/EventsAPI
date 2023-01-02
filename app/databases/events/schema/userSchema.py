from app import ma
from app.databases.events.models    import Users

from app.databases.events.schema .physicalPersonSchema import PhysicalPersonSchema
from app.databases.events.schema .legalPersonSchema import LegalPersonSchema
from app.databases.events.schema .genreTypesSchema import GenreTypeSchema

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

