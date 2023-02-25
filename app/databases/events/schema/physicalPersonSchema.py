from marshmallow import post_load,post_dump,validates_schema,pre_load,pre_dump,validates
from app.server.instance import app

from app.databases.events.models    import PhysicalPerson,GenreTypes
from app.databases.events.schema.genreTypesSchema import GenreTypeSchema
from app.utils.functions.validitys import validity_field

class PhysicalPersonSchema(app.ma.SQLAlchemyAutoSchema):
    genre_ship = app.ma.Nested(GenreTypeSchema)

    @post_load
    def new_physical(self,data,**kwargs):
        data.save()
        return data

    @validates_schema
    def unique_input(self,data,**kwargs):
        check = {'cpf':data['cpf']}
        validity_field.unique(PhysicalPerson,check)
        return data

    @validates('genre_id')
    def genre_exists(self,data,**kwargs):
        validity_field.find_field_model(GenreTypes,{'id':data,"status":True},'genre_id')

    class Meta:
        unknown = 'exclude'
        model = PhysicalPerson
        load_instance = True
        include_fk=True
        ordered = True
        dump_only = ("id",)