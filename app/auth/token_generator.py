from datetime import datetime,timedelta
from flask import jsonify
import jwt


class GenerateJWT:
    def __init__(self,key):
        self.SECRET_KEY = key
        self.EXP = 1140
        self.ALG = 'HS256'

    def get_token(self,_id,email):
        exp =  datetime.timestamp(datetime.now()+timedelta(minutes=self.EXP))
        dados={
            'some':{'id':_id,'email':email},
            'exp':exp}
        
        token_jwt = jwt.encode(dados,self.SECRET_KEY,algorithm=self.ALG)
        return token_jwt

    def token_required(self,token):
        if not token:
            return jsonify({'message':'Acesso não autorizado.','data':{},'error':401}),401
        try:
            token = str(token).replace('Bearer ','')
            data = jwt.decode(token,self.SECRET_KEY,algorithms=[self.ALG])

            time_actual = datetime.timestamp(datetime.now())
            if float(time_actual) >= float(data['exp']):
                return jsonify({'message':'Sua sessão expirou.','data':{},'error':401}),401
                
        except:
            return jsonify({'message':'Acesso negado.','data':{},'error':401}),401
            
        return jsonify({'jwt':data,'message':'success','error':0}),200,data

