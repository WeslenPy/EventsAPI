from app import ma
from app.models import Lots

class LotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lots
        unknown = "exclude"

        load_instance = True
