from tests import BASE_URL,HEADERS
from pytest import fixture,mark
from requests import request

BASE = f"{BASE_URL}/user/auth"


@mark.run(order=3)
@fixture(scope="session")
def headers():

    data = {"email":"weslenjhony@gmail.com","password":"weslen123"}
    response = request("POST",BASE,headers=HEADERS,json=data)

    headers = HEADERS.copy()
    token = response.json()['access_token']
    headers.update({"Authorization":f"Bearer {token}"})


    return headers


