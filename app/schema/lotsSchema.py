from app import ma
from app.models import Lots

class LotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lots
        load_instance = True
