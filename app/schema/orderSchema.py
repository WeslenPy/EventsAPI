from app import ma
from app.models import Orders

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        model = Orders
        load_instance = True
        ordered = True
        dump_only = ("id",)
