from typing import Dict, Union

from django.test import Client

from api.models import User


def create_test_account(client: Client,
                        first_name: str = "John",
                        last_name: str = "Doe",
                        password: str = "password123",
                        email: str = "johndoe@example.com",
                        return_json: bool = False,
                        login_user: bool = True) -> Union[User, Dict]:
    """
    Creates account via POST request to API and logs in user.
    :param client: The test case client used to make API.
    :param first_name: First name of account.
    :param last_name: Last name of account.
    :param password: Password of account
    :param email: Email of account.
    :param return_json: Whether to return json response. Defaults to False, user object returned on default.
    :return: The user object or JSON response.
    """
    # Create the account
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password
    }
    response = client.post('/account', payload, format='json')
    user_json = response.json()

    if response.status_code != 201:
        raise ValueError(f"Account creation failed: {response.content}")

    if login_user:
        # Log in the user
        login_payload = {
            "email": email,
            "password": password
        }
        login_response = client.post('/login', login_payload, format='json')
        if login_response.status_code != 200:
            raise ValueError(f"Login failed: {login_response.content}")

        token = login_response.data['access']  # Assuming the token is in 'access'

        # Set Authorization header for future requests
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    if return_json:
        return user_json
    user = User.objects.get(id=user_json["id"])
    return user
