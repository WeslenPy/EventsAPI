from flask import request,jsonify

from datetime import datetime,timedelta
from time import time

from app.utils.functions import decorators,validity_password,not_found,validity_user_block
from app import app,db,tokenSafe
from app.api import NumberAPI
from app.models import *
from app.schema import *


@app.route('/service/price',methods=['POST','GET'])
@decorators.authUserDecorator()
@decorators.validityDecorator(['country','service','operator'])
def server_get():
    try:
        data = request.json
        services = Service.query.filter_by(country_id=data['country'],
                        service_name_id=data['service'],status=True).join(
                            ServiceName,ServiceName.id==Service.service_name_id).join(
                            API,API.id==Service.api_id).join(
                            Country,Country.id==Service.country_id).add_columns(
                            API.api_url,API.api_key,ServiceName.symbol,
                            API.api_name,Service.amount,Service.api_id,
                            Service.sell_price,Country.number_country).all()

        result = not_found.checkContent(services)
        if result !=False:return result

        symbol_operator = Operator.query.filter_by(id=data['operator']).first()
        symbol_operator = 'any' if symbol_operator is None else symbol_operator.symbol

        services = ServiceSchema(many=True).dump(services)
        for index,service in enumerate(services):
            api_number = NumberAPI(service['api_url'],service['api_key'],operator=symbol_operator)
            services[index]['amount'] = api_number.get_stock(service['number_country'],service['symbol'])['amount']
        
            services[index].pop('number_country')
            services[index].pop('symbol')
            services[index].pop('api_key')
            services[index].pop('api_url')

        return jsonify({'data':services,'message':'success','error':0}),200

    except: return jsonify({"messge":'Nenhum serviço encontrado.','error':1}),404


@app.route('/country/api',methods=['POST','GET'])
@decorators.authUserDecorator()
@decorators.validityDecorator(['country','service'])
def api_service():

    data = request.json

    services_filter = Service.query.filter_by(
        country_id=data['country'],service_name_id=data['service'],status=True).join(
        API,API.id==Service.api_id).with_entities(API.api_name).distinct().add_columns(
        API.api_name,API.id).order_by(API.api_name.asc()).all()

    result = not_found.checkContent(services_filter)
    if result !=False:return result

    all_api =ApiSchema(many=True).dump(services_filter)

    return jsonify({'data':all_api,'message':'success','error':0}),200


@app.route('/country',methods=['POST','GET'])
@decorators.authUserDecorator()
@decorators.validityDecorator(['service'])
def country():
    data= request.json

    service_id= data['service']
    all_country = Service.query.filter_by(service_name_id=service_id,status=True).join(
            Country,Country.id==Service.country_id).with_entities(
                Country.country_name).distinct().add_columns(
                Country.id,Country.country_name).order_by(
                    Country.country_name.asc()).all()
    
    result = not_found.checkContent(all_country)
    if result !=False:return result

    operators = Operator.query.all()
    all_country = CountrySchema(many=True).dump(all_country)
    operators = OperatorSchema(many=True).dump(operators)

    return jsonify({'data':[all_country,operators],'message':'success','error':0}),200


@app.route('/concluded/number',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator(['purchased_id'])
def concluded_number(currentUser):
 
    id_purchased = request.json.get('purchased_id',None)
    purchased  = PurchasedService.query.filter_by(id=id_purchased,user_id=currentUser['some']['id'],status='ACTIVE').first()

    result = not_found.checkContent(purchased,"Número não encontrado.")
    if result !=False:return result

    purchased.status='CONCLUDED'
    db.session.commit()
    return jsonify({'data':{},'message':'Pedido concluido com sucesso.','error':0}),200
    
@app.route('/deleted/number',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator(['purchased_id'])
def deleted_number(currentUser):

    id_purchased = request.json.get('purchased_id',None)
    purchased  = PurchasedService.query.filter_by(id=id_purchased,user_id=currentUser['some']['id'],status='ACTIVE').first()
    
    result = not_found.checkContent(purchased,"Número não encontrado.")
    if result !=False:return result

    purchased.status='DELETED'
    db.session.commit()
    return jsonify({'data':{},'message':'Número deletado com sucesso.','error':0}),200

    
@app.route('/cancel/number',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator(['purchased_id'])
def cancel_number(currentUser):

    id_purchased = request.json.get('purchased_id',None)

    user = User.query.filter_by(id=currentUser['some']['id']).first()
    if user.cancellation_progress:
        return jsonify({'data':{},'message':'Você possui um cancelamento em andamento.','error':1,'status':False}),400

    purchased  = PurchasedService.query.filter_by(id=id_purchased,user_id=user.id,status='ACTIVE').join(
        API,API.id==PurchasedService.server_api).add_columns(
        PurchasedService.id,PurchasedService.status,PurchasedService.activation_id,
        PurchasedService.price,API.api_key,API.api_url).first()

    result = not_found.checkContent(purchased,'Falha no cancelamento.')
    if result !=False:return result

    user.cancellation_progress = True
    db.session.commit()

    cancel = NumberAPI(purchased.api_url,purchased.api_key)
    cancel = cancel.cancel_number(purchased.activation_id)


    if cancel['error'] == False:

        user.balance +=float(purchased.price)
        purchased = PurchasedService.query.filter_by(id=purchased.id).first()

        purchased.status = 'CANCEL'
        configBlock = BlockingRule.query.first()

        if int(user.cancellation_count) >= int(configBlock.cancellations_allowed):
            user.blocked_time = datetime.timestamp(datetime.now()+timedelta(minutes=configBlock.blocking_time_minutes))
            user.cancellation_count = 0
        
        lastCancel = CancellationPurchasedService.query.filter_by(user_id=user.id).order_by(
                                    CancellationPurchasedService.id.desc()).first()
        
        if lastCancel is None:
            userCancel = CancellationPurchasedService(user_id=user.id,purchased_service_id=purchased.id)
            db.session.add(userCancel)
            user.cancellation_progress = False
            db.session.commit()

            return jsonify( {'data':{},'message':'Número cancelado com sucesso.','error':0,'status':True}),200
            
        timeCancel = lastCancel.cancellation_time
        
        if float(time() - float(timeCancel)) <= configBlock.interval:
            user.cancellation_count+=1
        
        userCancel = CancellationPurchasedService(user_id=user.id,purchased_service_id=purchased.id)
        db.session.add(userCancel)
        user.cancellation_progress = False
        db.session.commit()

        return jsonify(
            {'data':{},
            'message':'Número cancelado com sucesso.',
            'error':0,'status':True}),200
    
    user.cancellation_progress = False
    db.session.commit()

    return jsonify({'data':{},'message':'Não foi possivel efetuar o cancelamento deste número.','error':1,'status':True}),400


@app.route('/buy/number',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({'service':int,'country':int,'api':int,'operator':int})
def buy_number_api(currentUser):
 
    dataResponse = request.json

    user = User.query.filter_by(id=currentUser['some']['id']).first()
    result = validity_user_block.validityBlockUser(user)
    if result !=False:return result
   
    idService = dataResponse['service']
    idAPI = dataResponse['api']
    idCountry = dataResponse['country']
    idOperator = dataResponse['operator']
    
    dataBuy = Service.query.filter_by(service_name_id=idService,api_id=idAPI,country_id=idCountry,status=True).join(
        Country, Country.id == Service.country_id).join(API,API.id==Service.api_id).join(
            ServiceName,ServiceName.id==Service.service_name_id).add_columns(
                Service.id,Service.sell_price,ServiceName.symbol,Service.api_id,
                    Country.number_country,API.api_url,API.api_key).first()

    result = not_found.checkContent(dataBuy,'Serviço indisponivel.')
    if result !=False:return result

    if float(user.balance) < float(dataBuy.sell_price):
        return jsonify({'data':{},'message':'Saldo insuficiente','error':1,'status':False})
    
    user.purchase_progress = True
    db.session.commit()

    operator = Operator.query.get(idOperator) 

    buyNumber = NumberAPI(dataBuy.api_url,dataBuy.api_key,operator.symbol)
    buyNumber = buyNumber.buy_number(dataBuy.symbol,dataBuy.number_country)

    if buyNumber['error']== True:
        user.purchase_progress = False
        db.session.commit()
        return jsonify({'data':{},'message':'Número indisponivel.','error':1,'status':False})
    

    new_purchased = PurchasedService(price=dataBuy.sell_price,status='ACTIVE',service_number=buyNumber['number'],operator_id=operator.id,
                                user_id=user.id,service_id=dataBuy.id,activation_id=buyNumber['id'],server_api=dataBuy.api_id)
    ServiceName.query.get(idService).more_buy +=1
    
    user.purchase_progress = False
    user.balance -=float(dataBuy.sell_price)
    db.session.add(new_purchased)
    db.session.commit()

    countPurchased = PurchasedService.query.filter_by(user_id=user.id).count()

    return jsonify({'data':{'balance':float(user.balance),'pieces':countPurchased},
                        'message':'Número comprado com sucesso','error':0,'status':True})


@app.route('/buy/number/repeat',methods=['POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({'id':int})
def buy_number_repeat(currentUser):
    dataResponse = request.json

    id_purchased = dataResponse['id']
    
    user = User.query.filter_by(id=currentUser['some']['id']).first()
    result = validity_user_block.validityBlockUser(user)
    if result !=False:return result
   

    purchased = PurchasedService.query.filter_by(id=id_purchased,user_id=user.id).join(
        Service,Service.id==PurchasedService.service_id).join(
            Operator,Operator.id==PurchasedService.operator_id).add_columns(
                    PurchasedService.server_api,PurchasedService.operator_id,
                    Service.country_id,Service.service_name_id,Operator.symbol).first()

    result = not_found.checkContent(purchased,'Compra não encontrada.')
    if result !=False:return result
    
    dataBuy = Service.query.filter_by(service_name_id=purchased.service_name_id,api_id=purchased.server_api,
                                        country_id=purchased.country_id,status=True).join(
                                        Country, Country.id == Service.country_id).join(API,API.id==Service.api_id).join(
                                            ServiceName,ServiceName.id==Service.service_name_id).add_columns(
                                                Service.id,Service.sell_price,ServiceName.symbol,Service.api_id,
                                                    Country.number_country,API.api_url,API.api_key).first()

                        
    result = not_found.checkContent(dataBuy,'Serviço indisponivel.')
    if result !=False:return result

    if float(user.balance) < float(dataBuy.sell_price):
        return jsonify({'data':{},'message':'Saldo insuficiente','error':1,'status':False}),200
    
    user.purchase_progress = True
    db.session.commit()

    buyNumber = NumberAPI(dataBuy.api_url,dataBuy.api_key,purchased.symbol)
    buyNumber = buyNumber.buy_number(dataBuy.symbol,dataBuy.number_country)

    if buyNumber['error']== True:
        user.purchase_progress = False
        db.session.commit()
        return jsonify({'data':{},'message':'Número indisponivel.','error':1,'status':False}),200

    purchased = PurchasedService(price=dataBuy.sell_price,status='ACTIVE',service_number=buyNumber['number'],operator_id=purchased.operator_id,
                                user_id=user.id,service_id=dataBuy.id,activation_id=buyNumber['id'],server_api=dataBuy.api_id)

    user.purchase_progress = False
    user.balance -=float(dataBuy.sell_price)
    db.session.add(purchased)
    db.session.commit()

    return jsonify({'data':{},'message':'Número comprado com sucesso','error':0,'status':True}),200


@app.route('/sms/historic',methods=['GET','POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({'id':int})
def sms_historic(currentUser):
    dataResponse = request.json

    smsAll = SmsHistory.query.filter_by(purchased_service_id=dataResponse['id'],user_id=currentUser['some']['id']).all()
    
    result = not_found.checkContent(smsAll)
    if result !=False:return result

    smsAll = HistoryCodeSchema(many=True).dump(smsAll)

    return jsonify({'data':smsAll,'message':'success','error':0,'status':True}),200
    

@app.route('/get/purchased',methods=['GET','POST'])
@decorators.authUserDecorator(True)
@decorators.validityDecorator({'id':int})
def get_purchased(currentUser):
  
    dataResponse = request.json
    getPurchased = PurchasedService.query.filter_by(id=dataResponse['id'],user_id=currentUser['some']['id']).join(
                                Service,Service.id==PurchasedService.service_id).join(
                                    Country,Country.id==Service.country_id).join(
                                    ServiceName,ServiceName.id==Service.service_name_id).add_columns(
                                         PurchasedService.id, PurchasedService.service_number, 
                                        PurchasedService.created_at, PurchasedService.status,
                                            ServiceName.name,Country.ddi).first()

    result = not_found.checkContent(getPurchased)
    if result !=False:return result

    getPurchased = PurchasedSchema().dump(getPurchased)

    return jsonify({'data':getPurchased,'message':'success','error':0,'status':True}),200


@app.route('/bot/balance/add/<token>',methods=['POST'])
def bot_balance_add(token):

    try:
        idPanel,passwordPanel,balance,*_ = tokenSafe.loads(token,salt='addBalanceBotForPainel',max_age=60)
        user  = User.query.get(idPanel)
    
        if user is None: return jsonify({'data':{},
                                        'message':'PIN de cliente não encontrado em nossos sistemas!',
                                        'error':1}),404

        if validity_password.comparePassword(passwordPanel,user.password):
            balance_before = user.balance
            user.balance+=float(balance)

            method = PaymentMethod.query.filter_by(method='Bot').first()
            new_transfer = RechargeHistory('bot_transfer',balance,'Transferencia via bot',
                                            user.id,payment_method_id=method.id,status='CONCLUDED')
            db.session.add(new_transfer)
            db.session.commit()

            return jsonify({"message":'Saldo transferido com sucesso!','error':0,
                            'data':{'before_balance':balance_before,
                                    'after_balance':user.balance,
                                    "email":user.email}}),200
       
        return jsonify({"message":'PIN de cliente ou senha invalido(s).','error':1}),400

    except:
        return jsonify({"message":'Tempo esgotado!','error':1}),400

