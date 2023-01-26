
from app.databases.events.schema import RulesEventSchema
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app
from app.utils.functions.decorators import auth

api = app.rules_api

rules_model =api.model('Rules', {
    "type":fields.String(description='Tipo da regra.',required=True,),
    "description":fields.String(description='Descrição da regra.',required=True,),
    "event_id":fields.Integer(description='Id do evento.',required=True,),
    "status":fields.Boolean(description='Status da regra.',default=True),
    "created_at":fields.DateTime(description="Data de criação.",readonly=True),

})
@api.route('/create')
class Rules(Resource):

    @api.expect(rules_model, validate=True)
    @api.doc("Rota para cadastro das regras do evento")
    @auth.authType(required=True,api=api)
    def post(self,**kwargs):
        data = api.payload
        _schema =  RulesEventSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Rule created successfully',
            'error':False},200
