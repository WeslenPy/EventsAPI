from app.server.instance import app

from app.databases.events.models    import GenreTypes
from marshmallow import post_load,validates
from app.utils.functions.validitys import validity_field
class GenreTypeSchema(app.ma.SQLAlchemyAutoSchema):


    @post_load
    def new_genre(self,data,**kwargs):
        data.save()
        return data

    @validates('type')
    def unique(self,data,**kwargs):
        validity_field.unique(GenreTypes,{"type":data})
        return data

    class Meta:
        model = GenreTypes
        ordered = True
        include_fk=True
        load_instance = True
        unknown = "exclude"
        dump_only = ("id",)