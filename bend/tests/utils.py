from typing import Dict, Union

from django.test import Client

from api.models import User


def create_test_account(client: Client,
                        first_name: str = "John",
                        last_name: str = "Doe",
                        password: str = "password123",
                        email: str = "johndoe@example.com",
                        return_json: bool = False) -> Union[User, Dict]:
    """
    Creates account via POST request to API.
    :param client: The test case client used to make API.
    :param first_name: First name of account.
    :param last_name: Last name of account.
    :param password: Password of account
    :param email: Email of account.
    :param return_json: Whether to return json response. Defaults to False, user object returned on default.
    :return: The user object.
    """
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password
    }
    response = client.post('/account', payload, format='json')
    user_json = response.json()
    if return_json:
        return user_json
    user = User.objects.get(id=user_json["id"])
    return user
