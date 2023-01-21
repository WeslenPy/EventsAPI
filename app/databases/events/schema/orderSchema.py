from app.server.instance import app

from app.databases.events.models    import Orders
from marshmallow import fields,validate

class OrderSchema(app.ma.SQLAlchemyAutoSchema):

    # status =fields.Str(validate=validate.OneOf(['Pending','Approved','Expired']))

    class Meta:
        unknown = "exclude"
        model = Orders
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
