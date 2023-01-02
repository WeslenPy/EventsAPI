import requests

class ApiBrasil:
    def __init__(self) -> None:
        self.baseURL = "https://brasilapi.com.br/api"

    def searchCEP(self,cep:int,city_compair:str,state:str):
        try:
            if len(str(cep))>8:return False,"cep is invalid"  
            elif len(state)>2:return False,"state is invalid"

            response =requests.get(f"{self.baseURL}/cep/v1/{cep}")
            data:dict = response.json()
            typeError = data.get('type',False)
            if typeError:return False,"cep is invalid"         

            city_cep = data.get('city','')
            state_cep = data.get('state','')
            if state.lower() != state_cep.lower():return False,"state does not match the zip code"
            elif city_compair.lower() != city_cep.lower():return False,"city does not match the zip code"

            return True,'cep is valid'
        except:return True,'cep is valid'


    

