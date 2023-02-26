
from tests import BASE_URL,HEADERS
from requests import request,Response


BASE  = f"{BASE_URL}/user"


def test_create_new_user_physical():
    """
    Testar se a criação de um novo usuario está funcionando.
    """

    data = {
            "email": "weslenjhony@gmail.com",
            "password": "weslen123",
            "phone": "5599985800340",
            "zip_code": "45205000",
            "address": "Avenida",
            "number_address": 23,
            "state": "MA",
            "complement": "casa",
            "district": "centro",
            "city": "Cidade Nova",
            "cpf": "41610032004",
            "full_name": "Weslen Jhony",
            "birth_date": "2023-01-22T23:40:33.846Z",
            "genre_id": 1
    }

    response:Response = request("POST",f"{BASE}/physical",json=data,headers=HEADERS)

    assert response.status_code == 200,"Tudo certo"
    


def test_create_new_user_corporate():
    """
    Testa a criação de conta pessoa juridica 
    """

    data = {
            "email": "enterprise@gmail.com",
            "password": "weslen123",
            "phone": "5599985400340",
            "zip_code": "45205000",
            "address": "Avenida",
            "number_address": 23,
            "state": "MA",
            "complement": "casa",
            "district": "centro",
            "city": "Cidade Nova",
            "cnpj": "87148504000131",
            "corporate_name": "Empresa Ingressos",
    }

    response:Response = request("POST",f"{BASE}/corporate",json=data,headers=HEADERS)
    data = response.json()

    assert response.status_code == 200,'Tudo certo.'    