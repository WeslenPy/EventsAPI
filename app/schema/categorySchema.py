from app import ma
from app.models import Category

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
