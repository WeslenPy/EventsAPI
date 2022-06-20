
from app.utils.functions import decorators
from flask import request,jsonify
from datetime import datetime
from app import app

from app.models import GenreTypes
from app.schema import GenreTypeSchema


"""
POST REGISTER DATA 
"""

@app.route('/api/v1/create/genre',methods=['POST'])
# @decorators.authUserDecorator(is_admin=True)
@decorators.validityDecorator({'type':str,'description':str,"status":bool})
def create_genre():
    data = request.get_json()

    genreFind =GenreTypes.query.filter(GenreTypes.type==data['type']).first()
    if not genreFind:
        genre:GenreTypes = GenreTypeSchema().load(data)
        genre.save()

        genreData = GenreTypeSchema().dump(genre)
        return jsonify({'status':200,'message':'genre created successfully','data':genreData,'success':True}),200

    genreData = GenreTypeSchema().dump(genreFind)
    return jsonify({'status':200,'message':'genre has already been registered','data':genreData,'success':False}),200
    
   

@app.route('/api/v1/get/genres',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_genres():

    genres:GenreTypes = GenreTypes.query.all()
    genres = GenreTypeSchema(many=True).dump(genres)

    return  jsonify({'status':200,'message':'success','data':genres,'success':True}),200

@app.route('/api/v1/get/genre/<int:id_genre>',methods=['GET'])
# @decorators.authUserDecorator(is_admin=True)
def get_genre(id_genre):

    genre:GenreTypes = GenreTypes.query.get(id_genre)
    genre = GenreTypeSchema().dump(genre)

    return  jsonify({'status':200,'message':'success','data':genre,'success':True}),200

