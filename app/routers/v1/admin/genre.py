
from app.databases.events.models    import GenreTypes
from app.databases.events.schema  import GenreTypeSchema

from flask_restx import Resource,Api,fields
from marshmallow import ValidationError
from app.server import app

api:Api = app.admin_api
genre_model =api.model('Genre',{
                            'type':fields.String(required=True,description="Tipo do genero"),
                            'description':fields.String(description="Descrição do genero"), 
                            })


@api.route("/create/genre")
class GenreTypes(Resource):
    
    @api.expect(genre_model,validate=True)
    @api.doc("Rota para cadastrar generos")
    def post(self,**kwargs):
        data = api.payload
        _schema =  GenreTypeSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'status':200,
            'message':'Genre created successfully',
            'error':False},200
# """
# POST REGISTER DATA 
# """

# @v1.route('create/genre',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
# @decorators.validityDecorator({'type':str,'description':str,"status":bool})
# def create_genre():
#     data = request.get_json()

#     genreFind =GenreTypes.query.filter(GenreTypes.type==data['type']).first()
#     if not genreFind:
#         genre:GenreTypes = GenreTypeSchema().load(data)
#         genre.save()

#         genreData = GenreTypeSchema().dump(genre)
#         return jsonify({'status':200,'message':'genre created successfully','data':genreData,'success':True}),200

#     genreData = GenreTypeSchema().dump(genreFind)
#     return jsonify({'status':200,'message':'genre has already been registered','data':genreData,'success':False}),200
    

# @v1.route('get/genres',methods=['GET'])
# def get_genres():

#     genres:GenreTypes = GenreTypes.query.all()
#     genres = GenreTypeSchema(many=True).dump(genres)

#     return  jsonify({'status':200,'message':'success','data':genres,'success':True}),200

# @v1.route('get/genre/<int:id_genre>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_genre(id_genre):

#     genre:GenreTypes = GenreTypes.query.get(id_genre)
#     genre = GenreTypeSchema().dump(genre)

#     return  jsonify({'status':200,'message':'success','data':genre,'success':True}),200

