from app import ma
from app.models import PhysicalPerson

class PhysicalPersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = 'exclude'
        model = PhysicalPerson
        load_instance = True
        ordered = True
        dump_only = ("id",)