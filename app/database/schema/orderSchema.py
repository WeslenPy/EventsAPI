from app import ma
from app.database.models    import Orders
from marshmallow import fields,validate

class OrderSchema(ma.SQLAlchemyAutoSchema):

    # status =fields.Str(validate=validate.OneOf(['Pending','Approved','Expired']))

    class Meta:
        unknown = "exclude"
        model = Orders
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
