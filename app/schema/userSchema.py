from app import ma
from app.models import Users,PhysicalPerson,LegalPerson,GenreTypes

class UserSchema(ma.SQLAlchemyAutoSchema):
    
    physical_person = ma.Nested(PhysicalPerson)
    legal_person = ma.Nested(LegalPerson)
    genre = ma.Nested(GenreTypes)
    
    class Meta:
        unknown = "exclude"
        ordered = True
        model = Users
        load_instance = True
