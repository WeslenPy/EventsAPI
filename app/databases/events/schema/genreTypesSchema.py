from app.server.instance import app

from app.databases.events.models    import GenreTypes
from marshmallow import post_load,validates
from app.utils.functions.validitys import validity_field
from flask_restx import fields



api = app.admin_api

genre_model =api.model('Genre',{
                        'id':fields.Integer(readonly=True,description="Id do genero"),
                        'type':fields.String(required=True,description="Tipo do genero"),
                        'description':fields.String(description="Descrição do genero"), 
                        'status':fields.Boolean(readonly=True,description="Status do genero",default=True), 
                        'created_at':fields.DateTime(readonly=True,description="Data de criação"), 
                        })
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


