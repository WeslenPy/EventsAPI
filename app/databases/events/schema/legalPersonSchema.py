from app.server.instance import app

from app.databases.events.models    import LegalPerson
from marshmallow import post_load
class LegalPersonSchema(app.ma.SQLAlchemyAutoSchema):

    @post_load
    def _new(self,data,**kwargs):
        data.save()
        return data


    class Meta:
        unknown = "exclude"
        ordered = True
        model = LegalPerson
        include_fk=True
        load_instance = True
        dump_only = ("id",)
