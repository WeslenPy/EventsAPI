from app.models import PhysicalPerson,Users,LegalPerson
from app.utils.functions.validitys import validatyCPF
from flask import jsonify

def validityAlready(data:dict,attr='cpf'):

    if attr=='cpf':
        if PhysicalPerson.query.filter_by(cpf=data['cpf']).first():
            return ({'status':200,
                    'message':'CPF has already been registered.',
                    'success':False}),200
        
        cpf =  validatyCPF(data['cpf'])
        if not cpf:
            return ({'status':200,
                'message':'CPF is invalid.',
                'success':False}),200
        data['cpf'] =cpf

    elif attr=='cnpj':
        if LegalPerson.query.filter_by(cnpj=data['cnpj']).first():
            return ({'status':200,
                'message':'CNPJ has already been registered.',
                'success':False}),200

    elif Users.query.filter_by(email=data['email']).first():
        return jsonify({'status':200,
                        'message':'Email has already been registered.',
                        'success':False}),200 
    
    elif Users.query.filter_by(phone=data['phone']).first():
        return jsonify({'status':200,
                        'message':'Phone has already been registered.',
                        'success':False}),200

    return False