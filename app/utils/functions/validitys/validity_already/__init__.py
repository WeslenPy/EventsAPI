from app.models import PhysicalPerson,Users,LegalPerson,GenreTypes
from app.utils.functions.validitys import validityCPF,validityCNPJ
from app import brasil_api
from flask import jsonify


def validityAlready(data:dict,attr='cpf'):

    if attr=='cpf':
        if PhysicalPerson.query.filter_by(cpf=data['cpf']).first():
            return ({'status':400,
                    'message':'CPF has already been registered.',
                    'success':False}),400
        
        cpf =  validityCPF(data['cpf'])
        if not cpf:
            return ({'status':400,
                'message':'CPF is invalid.',
                'success':False}),400
        data['cpf'] =cpf

    elif attr=='cnpj':
        if LegalPerson.query.filter_by(cnpj=data['cnpj']).first():
            return ({'status':400,
                'message':'CNPJ has already been registered.',
                'success':False}),400

        cnpj =  validityCNPJ(data['cnpj'])
        if not cnpj:
            return ({'status':400,
                'message':'cnpj is invalid.',
                'success':False}),400
                
        data['cnpj'] =cnpj

    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'status':400,
                        'message':'Email has already been registered.',
                        'success':False}),400 
    
    elif Users.query.filter_by(phone=data['phone']).first():
        return jsonify({'status':400,
                        'message':'Phone has already been registered.',
                        'success':False}),400 

        
                        
    elif len(str(data['phone']))<11 or len(str(data['phone']))<13:
        return jsonify({'status':400,
                        'message':'Invalid number phone',
                        'success':False}),400   

    elif attr=='cpf' and not GenreTypes.query.get(data['genre_id']):
        return jsonify({'status':400,
                        'message':'Invalid genre_id',
                        'success':False}),400

    validity = brasil_api.searchCEP(data['cep'],data['city'],data['state'])
    if not validity[0]: 
        return jsonify({'status':400,
                        'message':validity[1],
                        'success':False}),400

    if len(data['password']) <8:
        return jsonify({'status':400,
                        'message':'invalid password, your password must be at least 8 characters long',
                        'success':False}),400


    return False