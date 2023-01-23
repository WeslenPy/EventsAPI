
from app.databases.events.schema  import GenreTypeSchema,genre_model
from flask_restx import Resource,Api
from marshmallow import ValidationError
from app.server import app

api:Api = app.admin_api


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


# @v1.route('get/genres',methods=['GET'])
# def get_genres():

#     genres:GenreTypes = GenreTypes.query.all()
#     genres = GenreTypeSchema(many=True).dump(genres)

#     return  jsonify({'status':200,'message':'success','data':genres,'success':True}),200

