from app.server.instance import app

from app.databases.events.models    import Orders
from marshmallow import post_load
class OrderSchema(app.ma.SQLAlchemyAutoSchema):

    # status =fields.Str(validate=validate.OneOf(['Pending','Approved','Expired']))
    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data

    class Meta:
        unknown = "exclude"
        model = Orders
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
