
from app.databases.events.schema import PartnerSchema
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app
from app.utils.functions.decorators import auth

api = app.partner_api

partener_model =api.model('Partner', {
    "event_id":fields.Integer(description='Id do evento.',required=True,),
    "user_id":fields.Integer(description='Id do partner(user_id).',required=True,),
    "status":fields.Boolean(description='Status do partner.',default=True),
    "created_at":fields.DateTime(description="Data de criação.",readonly=True),

})
@api.route('/create')
class Partener(Resource):

    @api.expect(partener_model)
    @api.doc("Rota para cadastro dos parceiros")
    @auth.authType(required=True,api=api)
    def post(self,**kwargs):
        data = api.payload
        _schema =  PartnerSchema()

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Partner created successfully',
            'error':False},200
