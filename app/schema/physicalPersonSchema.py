from app import ma
from app.models import PhysicalPerson
from marshmallow import EXCLUDE

class PhysicalPersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = EXCLUDE
        model = PhysicalPerson
        load_instance = True
