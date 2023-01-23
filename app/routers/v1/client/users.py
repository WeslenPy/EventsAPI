from app.databases.events.schema import UserSchema,PhysicalPersonSchema,LegalPersonSchema
from flask_restx import Resource,Api,fields
from marshmallow import ValidationError
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

user_corporate = api.clone("Coporate",user_model,{
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
            'status':200,
            'message':'Link send to email',
            'error':False},200
@api.route("/coporate")
class Coporate(Resource):
    
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
            'status':200,
            'message':'Link send to email',
            'error':False},200

        

# @v1.route('register/physical',methods=['POST'])
# @decorators.validityDecorator({'email':str,'password':str,'phone':int,'cep':int,
#                                 'address':str,'number_address':int,'state':str,
#                                 'complement':str,'district':str,'city':str,'cpf':str,
#                                 'full_name':str,'birth_date':datetime,'genre_id':int})
# def register_physical():

#     data = request.get_json()

#     result = validitys.validityAlready(data,'cpf')
#     if result:return result

#     physical:PhysicalPerson = PhysicalPersonSchema().load(data)
#     physical.save()

#     data['physical_id'] = physical.id

#     try:new_user:Users = UserSchema().load(data)
#     except ValidationError as err: 
#         physical = PhysicalPerson.query.get(physical.id)
#         db.session.delete(physical)
#         db.session.commit()
#         message = error_messages.parseMessage(err.messages)
#         return jsonify({'status':400,'message':message,'success':False}),400

#     new_user.save()
    


# #     token_url = tokenSafe.dumps(data['email'],salt='emailConfirmUser')
# #     msg = Message("Não responda este e-mail",
# #             sender=app.config['MAIL_USERNAME'],
# #             recipients=[data['email']])

# #     url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
# #     msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=data['full_name']))
# #     executor.submit(mail.send,msg)
    
#     return jsonify({
#             'status':200,
#             'message':'Link send to email',
#             'success':True}),200



# @v1.route('register/juridical',methods=['POST'])
# @decorators.validityDecorator({'email':str,'password':str,'phone':int,
#                                 'cep':int,'address':str,'number_address':int,
#                                 'complement':str,'district':str,'city':str,'cnpj':str,
#                                 "corporate_name":str,'state':str})
# def register_legal():

#     data =  request.get_json()
#     result = validitys.validityAlready(data,'cnpj')
#     if result:return result

#     new_juridical:LegalPerson = LegalPersonSchema().load(data)
#     new_juridical.save()

#     data['legal_id'] = new_juridical.id
#     try:new_user:Users = UserSchema().load(data)
#     except ValidationError as err: 
#         juridical = LegalPerson.query.get(new_juridical.id)
#         db.session.delete(juridical)
#         db.session.commit()
#         message = error_messages.parseMessage(err.messages)

#         return jsonify({'status':400,'message':message,'success':False}),400

#     new_user.save()

#     # token_url = tokenSafe.dumps(data['email'],salt='emailConfirmUser')
#     # msg = Message("Não responda este e-mail",
#     #         sender=app.config['MAIL_USERNAME'],
#     #         recipients=[data['email']])

#     # url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
#     # msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=data['corporate_name']))
#     # executor.submit(mail.send,msg)
    
#     return jsonify({
#             'status':200,
#             'message':'Link send to your email',
#             'success':True}),200

# """
# CHANGE DATA TABLE
# """
# @v1.route('edit/user/physical/<int:id_user>',methods=['PUT'])
# @decorators.authUserDecorator()
# def edit_physical(id_user):


#     data = request.get_json() 
#     if not data:
#         return jsonify({
#             'status':404,
#             'message':'fields not found',
#             'success':False}),200

#     edit_user:Users = Users.query.get(id_user)
#     if edit_user:
#         edit_physical:PhysicalPerson = PhysicalPerson.query.get(edit_user.physical_id)

#         edit_user.update(data)
#         edit_physical.update(data)

#         edit_user = UserSchema().dump(edit_user)

#         return jsonify({
#             'status':200,
#             'message':'user update successfully',
#             'data':edit_user,
#             'success':True}),200


#     return jsonify({
#             'status':404,
#             'message':'user not found',
#             'success':False}),200



# """
# DELETE USER API DATA 
# """
# @v1.route('delete/user/<int:id_user>',methods=['DELETE'])
# @decorators.authUserDecorator()
# def delete_user(id_user):

#     user:Users = Users.query.get(id_user)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
    
#         return  jsonify({'status':200,'message':'success','success':True}),200

#     return  jsonify({'status':404,'message':'user not found','success':False}),404


# """
# GET API DATA ALL
# """

# @v1.route('get/users',methods=['GET'])
# @decorators.authUserDecorator()
# def get_users():

#     users:Users = Users.query.all()
#     users = UserSchema(many=True).dump(users)

#     return  jsonify({'status':200,'message':'success','data':users,'success':True}),200
    
    
    
# @v1.route('get/user/<int:id_user>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_user(id_user):

#     user:Users = Users.query.get(id_user)
#     if user:
#         user = UserSchema().dump(user)

#         return  jsonify({'status':200,'message':'success','data':user,'success':True}),200

#     return  jsonify({'status':404,'message':'user not found','success':False}),404
    
    
# @v1.route('get/user/events/<int:id_user>',methods=['GET'])
# @decorators.authUserDecorator()
# def get_user_events(id_user):

#     event:Events = Events.query.filter_by(user_id=id_user).all()
#     if event:
#         event = EventSchema(many=True).dump(event)

#         return  jsonify({'status':200,'message':'success','data':event,'success':True}),200

#     return  jsonify({'status':404,'message':'events not found','success':False}),404
