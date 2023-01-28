from app.databases.events.schema import UserSchema,PhysicalPersonSchema,LegalPersonSchema
from app.databases.events.models import Users
from flask_restx import Resource,Api,fields
from marshmallow import ValidationError
from app.utils.functions.decorators import auth
from app.server import app

api:Api = app.user_api
user_model =api.model('User',{
                            'email':fields.String(required=True,description="Email valido"),
                            'password':fields.String(required=True,description="Senha",min_length=8),
                            'phone':fields.String(required=True,description="Número de telefone",max_length=20),
                            'zip_code':fields.String(required=True,description="CEP da cidade.",min_length=8,max_length=8),
                            'address':fields.String(required=True,description="Endereço real"),
                            'number_address':fields.Integer(required=True,description="Número da casa"),
                            'state':fields.String(required=True,description="Estado",min_length=2,max_length=2), 
                            'complement':fields.String(required=True,description="Complemento"),
                            'district':fields.String(required=True,description="Bairro"),
                            'city':fields.String(required=True,description="Cidade"),
                           
                            })

user_physical = api.clone("Physical",user_model,{
                            'cpf':fields.String(required=True,description="Identificação CPF",min_length=11,max_length=11),
                            'full_name':fields.String(required=True,description="Nome completo"),
                            'birth_date':fields.DateTime(required=True,description="Data de aniversario"),
                            'genre_id':fields.Integer(required=True,description="Id do genero"),
})

user_corporate = api.clone("Corporate",user_model,{
                            'cnpj':fields.String(required=True,description="Identificação CNPJ",min_length=14,max_length=14),
                            'corporate_name':fields.String(required=True,description="Nome fantasia da empresa"),
})


@api.route("/physical")
class Phisycal(Resource):
    
    @api.expect(user_physical,validate=True)
    @api.doc("Rota para cadastrar usuários(PF)",security=None)
    def post(self,**kwargs):
        data = api.payload
        _schema =  UserSchema(context={"type":PhysicalPersonSchema,"field":"physical_id"})

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Link send to email',
            'error':False},200

@api.route("/coporate")
class Corporate(Resource):
    
    @api.expect(user_corporate,validate=True)
    @api.doc("Rota para cadastrar usuários(PJ)",security=None)
    def post(self,**kwargs):
        data = api.payload
        _schema =  UserSchema(context={"type":LegalPersonSchema,"field":"legal_id",'type_user':False})

        try:data= _schema.load(data)
        except ValidationError as erros:
            return {"error":True,"message":"Algo deu errado.",
                                "details":{"erros":erros.messages}},201

        return {
            'code':200,
            'message':'Link send to email',
            'error':False},200

        

@api.route('/profile')
class UserProfileRouter(Resource):

    @api.doc("Rota para pegar todos os dados do usuário")
    @api.response(401,"Unauthorized")
    @api.response(200,"Success")
    @auth.authType(required=True,location='params')
    def get(self,**kwargs):
        
        items = Users.query.filter_by(active=True,id=kwargs['user_id']).all()
        data = UserSchema().dump(items)

        return {"message":"Success","data":data,"code":200,"error":False},200
