from app import ma
from app.models import LegalPerson

class LegalPersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"

        model = LegalPerson
        load_instance = True
