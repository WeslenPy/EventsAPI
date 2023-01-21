from app.server.instance import app

from app.databases.events.models    import Users

from app.databases.events.schema.physicalPersonSchema import PhysicalPersonSchema
from app.databases.events.schema.legalPersonSchema import LegalPersonSchema
from app.databases.events.schema.genreTypesSchema import GenreTypeSchema
from app.databases.events.schema.termsEventSchema import TermsEventSchema
from app.databases.events.schema.userAccessTypesSchema import UserAccessTypesSchema

class UserSchema(app.ma.SQLAlchemyAutoSchema):
    
    physical_ship = app.ma.Nested(PhysicalPersonSchema)
    legal_ship = app.ma.Nested(LegalPersonSchema)
    genre_ship = app.ma.Nested(GenreTypeSchema)
    
    types_children = app.ma.Nested(UserAccessTypesSchema,many=True)
    terms_children = app.ma.Nested(TermsEventSchema,many=True)

    email = app.ma.Email()
    
    class Meta:
        unknown = "exclude"
        model = Users

        load_instance = True
        include_fk=True
        ordered = True

        load_only = ("password",)
        dump_only = ("id",)

