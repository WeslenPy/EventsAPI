from flask import render_template,request,jsonify,session
from flask_mail import Message

from sqlalchemy.sql import functions

from app.utils.functions import decorators,not_found,validity_cpf
from app import app,db,tokenSafe,executor,mail
from app.api import NumberAPI
from app.models import *
from app.schema import *


@app.route('/register',methods=['POST'])
@decorators.validityDecorator({'first_name':str,'last_name':str,'email':str,'password':str})
def register():

    data = request.json

    first_name = str(data['first_name']).strip()
    last_name = str(data['last_name']).strip()
    email = str(data['email']).strip()
    password = str(data['password'])

    if User.query.filter_by(email=email).first():
        return jsonify({'message':'Email já foi cadastrado.','error':1}),401

    user = User(first_name=first_name,last_name=last_name,password=password,
                email=email)

    db.session.add(user)
    db.session.commit()

    token_url = tokenSafe.dumps(email,salt='emailConfirmUser')
    msg = Message("Não responda este e-mail",
            sender="noreply@meunumerovirtual.com",
            recipients=[email])

    url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')
    
    msg.html = str(render_template('confirm_email.html',url_validity=url_root,username=first_name))
    executor.submit(mail.send,msg)
    
    session['admin_logger'] = [False,False]

    return jsonify({
            'status':200,
            'message':'Enviamos um link de confirmação para seu e-mail, acesse-o para ativar sua conta!',
            'error':0}),200



@app.route('/user/profile',methods=['GET'])
@decorators.authUserDecorator(True)
def user_profile(currentUser):

    user = User.query.filter_by(id=currentUser['some']['id']).first()
    pieces = PurchasedService.query.filter_by(user_id=user.id).count()

    if pieces is None: pieces = 0

    serviceMin = db.session.query(functions.min(Service.sell_price)).join(
    ServiceName,ServiceName.id==Service.service_name_id).join(
    Country,Country.id==Service.country_id).join(
        API,API.id==Service.api_id).join(Color,Color.id==ServiceName.color_id
        ).group_by(Service.service_name_id).add_columns(

        ServiceName.id,ServiceName.name,ServiceName.symbol,
        ServiceName.url_image,Color.color_hex,
        API.api_key,API.api_url,Country.number_country,
        Service.service_name_id).order_by(ServiceName.more_buy.desc()).all()


    result = not_found(serviceMin,'Nenhum registro encontrado.')
    if result!=False: return result

    minValue = serviceMin
    serviceMin = ServiceSchema(many=True).dump(serviceMin)
    
    for index,data in enumerate(serviceMin):
        stock = NumberAPI(data['api_url'],data['api_key']).get_stock(data['number_country'],data['symbol'])
        serviceMin[index]['stock'] = stock['amount']
        serviceMin[index]['value'] = minValue[index][0]
        
        serviceMin[index].pop('api_key')
        serviceMin[index].pop('api_url')

    user_data = UserSchema().dump(user)
    user_data['pieces'] = pieces

    return jsonify({'data':user_data,'services':serviceMin}),200


@app.route('/user/update',methods=['PUT'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({"cpf":str})
def userUpdate(currentUser):
   
    dataResponse = request.json

    user = User.query.filter_by(id=currentUser['some']['id']).first()
    result= not_found.checkContent(user,'Usuario não encontrado')
    if result!=False:return result

    elif user.cpf is not None:
        if len(user.cpf) ==11:
            return jsonify({'data':{},'status':False,'message':'Seu CPF já está cadastrado. ','error':1}),200

    cpf = str(dataResponse['cpf']).replace('-','').replace('.','')

    searchCPF  = User.query.filter_by(cpf=cpf).first()
    if searchCPF: return jsonify({'data':{},'status':False,'message':'CPF não pode ser cadastrado.','error':1}),401

    validity = validity_cpf.validatyCPF(str(cpf))
    if validity:
        user.cpf = cpf
        db.session.commit()
        return jsonify({'data':{},'status':True,'message':'success','error':0}),200

    return jsonify({'data':{},'status':False,'message':'CPF invalido','error':1}),301


@app.route('/user/history',methods=['GET'])
@decorators.authUserDecorator(True)
def user_history(currentUser):

    dataHistory = PurchasedService.query.filter(PurchasedService.status=='ACTIVE').join(
                    Service, Service.id==PurchasedService.service_id).join(
                        Country,Country.id==Service.country_id).join(
                        ServiceName,ServiceName.id==Service.service_name_id).join(
                        API,API.id==PurchasedService.server_api).add_columns(
                                PurchasedService.id, PurchasedService.service_number,Country.ddi,
                                PurchasedService.created_at, PurchasedService.status,
                                    ServiceName.name,ServiceName.url_image,
                                    Service.service_name_id,API.api_name).filter(
                                            PurchasedService.user_id == currentUser['some']['id']).filter(
                                                API.id==PurchasedService.server_api).order_by(
                                                    PurchasedService.status.asc()).all()

    result= not_found.checkContent(dataHistory,'Nenhum número encontrado')
    if result!=False:return result

    dataHistory = HistoryCodeSchema(many=True).dump(dataHistory)

    for index,purchased in enumerate(dataHistory):
        sms = SmsHistory.query.filter_by(purchased_service_id=purchased['id']).order_by(SmsHistory.id.desc()).limit(1).first()
        if sms is None:
            dataHistory[index]['sms'] =None
            dataHistory[index]['received_at'] = None
        else:
            dataHistory[index]['sms'] = sms.sms
            dataHistory[index]['received_at'] = sms.received_at.strftime('%d-%m-%Y H %H:%M:%S')

    
    return jsonify({"data":dataHistory, 'message':'success','error':0,'status':True}),200



@app.route('/user/all/historic',methods=['GET'])
@decorators.authUserDecorator(True)
def user_historic_all(currentUser):

    dataHistory = PurchasedService.query.filter(
        PurchasedService.status!='ACTIVE').filter(
            PurchasedService.status!='DELETED').join(
                    Service, Service.id==PurchasedService.service_id).join(
                        Country,Country.id==Service.country_id).join(
                        ServiceName,ServiceName.id==Service.service_name_id).join(
                        API,API.id==PurchasedService.server_api).add_columns(
                                PurchasedService.id, PurchasedService.service_number,Country.ddi,
                                PurchasedService.created_at, PurchasedService.status,
                                    ServiceName.name,ServiceName.url_image,API.api_name).filter(
                                            PurchasedService.user_id == currentUser['some']['id']).filter(
                                                API.id==PurchasedService.server_api).order_by(
                                                    PurchasedService.created_at.desc()).all()

    result= not_found.checkContent(dataHistory,'Nenhum número encontrado')
    if result!=False:return result

    dataHistory = HistoryCodeSchema(many=True).dump(dataHistory)

    for index,purchased in enumerate(dataHistory):
        sms = SmsHistory.query.filter_by(purchased_service_id=purchased['id']).order_by(SmsHistory.id.desc()).limit(1).first()
        if sms is None:
            dataHistory[index]['sms'] =None
            dataHistory[index]['received_at'] = None
        else:
            dataHistory[index]['sms'] = sms.sms
            dataHistory[index]['received_at'] = sms.received_at.strftime('%d-%m-%Y H %H:%M:%S')
    
    return jsonify({"data":dataHistory, 'message':'success','error':0,'status':True}),200