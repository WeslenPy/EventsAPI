
from app.databases.events.schema import TermsEventSchema
from app.databases.events.models import TermsEvent
from werkzeug.datastructures import FileStorage
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app
from app.utils.functions.decorators import auth

api = app.terms_api


terms_parser = api.parser()
terms_parser.add_argument('term_file', location='files',help="Termo do evento.",
                           type=FileStorage, required=True)
terms_parser.add_argument('type_term', location='form',help="Tipo do termo.",
                           type=str, required=True)
terms_parser.add_argument('description', location='form',help="Descrição do termo.",
                           type=str, required=True)
terms_parser.add_argument('event_id', location='form',help="Id do evento.",
                           type=int, required=True)                           
terms_parser.add_argument('status', location='form',help="Status do termo.",
                           type=bool, required=False,default=True)


@api.route('/create')
class TermRouter(Resource):

    @api.expect(terms_parser)
    @api.doc("Rota para cadastro dos termos")
    @auth.authType(required=True,api=api)
    def post(self,**kwargs):
        data = terms_parser.parse_args()
        _schema =  TermsEventSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Term created successfully',
            'error':False},200

@api.route('/all')
class TermsRouter(Resource):

    @api.doc("Rota para pegar todos os termos do evento")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success")
    @auth.authType()
    def get(self,**kwargs):
        
        items = TermsEvent.query.filter_by(status=True).all()
        data = TermsEventSchema(many=True).dump(items)

        return {"message":"Success","data":data,"code":200,"error":False},200
