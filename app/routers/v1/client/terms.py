
from app.databases.events.schema import TermsEventSchema
from werkzeug.datastructures import FileStorage
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app

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
class Terms(Resource):

    @api.expect(terms_parser)
    @api.doc("Rota para cadastro ds termos")
    # @jwt_required()
    def post(self,**kwargs):
        data = terms_parser.parse_args()
        _schema =  TermsEventSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'status':200,
            'message':'Term created successfully',
            'error':False},200

