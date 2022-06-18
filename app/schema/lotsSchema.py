from app import ma
from app.models import Lots

class LotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lots
        unknown = "exclude"
        ordered = True
        load_instance = True
