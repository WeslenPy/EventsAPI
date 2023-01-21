from app.server.instance import app
from app.databases.events.models    import Category

class CategorySchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        model = Category
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
