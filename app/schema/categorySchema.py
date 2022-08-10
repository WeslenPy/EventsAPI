from app import ma
from app.models import Category

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        model = Category
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
