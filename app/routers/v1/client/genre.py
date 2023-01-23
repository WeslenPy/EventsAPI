
from app.databases.events.schema  import GenreTypeSchema,genre_model
from app.databases.events.models    import GenreTypes

from flask_restx import Resource,Api
from app.server import app

api:Api = app.genre_api



@api.route("/all")
class Genre(Resource):
    
    @api.doc("Lista de generos",security=None)
    @api.marshal_list_with(genre_model)
    def get(self):

        data:list[GenreTypes] = GenreTypes.query.filter_by(status=True).all()
        _schema:GenreTypeSchema =  GenreTypeSchema(many=True)
        data= _schema.dump(data)


        return data,200
