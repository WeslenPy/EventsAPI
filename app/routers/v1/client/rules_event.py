
from app.databases.events.schema import RulesEventSchema
from app.databases.events.models import RulesEvent
from flask_restx import Resource,fields
from marshmallow import ValidationError
from app.server import app
from app.utils.functions.decorators import auth

api = app.rules_api

rule_model =api.model('Rule', {
    "type":fields.String(description='Tipo da regra.',required=True,),
    "description":fields.String(description='Descrição da regra.',required=True,),
    "event_id":fields.Integer(description='Id do evento.',required=True,),
    "status":fields.Boolean(description='Status da regra.',default=True),
    "created_at":fields.DateTime(description="Data de criação.",readonly=True),

})

rules_model = api.clone("Rules",app.default_model,{
        "data":fields.Nested(rule_model,description="Todas as regras do evento",as_list=True)
})



@api.route('/create')
class RuleRouter(Resource):

    @api.doc("Rota para cadastro das regras do evento")
    @api.expect(rule_model, validate=True)
    @api.response(401,"Unauthorized")
    @api.response(200,"Success")
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

@api.route('/all')
class RulesRouter(Resource):

    @api.doc("Rota para pegar todos as regras do evento")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success",rules_model)
    @auth.authType()
    def get(self,**kwargs):
        
        items = RulesEvent.query.filter_by(status=True).all()
        data = RulesEventSchema(many=True).dump(items)

        return {"message":"Success","data":data,"code":200,"error":False},200


