from tests import BASE_URL
from requests import request


BASE = f"{BASE_URL}/ticket"


def test_create_ticket(headers):


    data = {
        "title": "Ticket Test",
        "price": 1,
        "description": "teste ticket",
        "max_buy": 1,
        "min_buy": 1,
        "paid": True,
        "status": True
    }

    response = request("POST",f"{BASE}/create",headers=headers,json=data)
    print(response.json())

    assert response.status_code == 200


