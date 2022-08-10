from app import ma
from app.models import LegalPerson

class LegalPersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = LegalPerson
        include_fk=True
        load_instance = True
        dump_only = ("id",)
