from rest_framework import status
from rest_framework.test import APITestCase


class AccountTest(APITestCase):
    def test_create_account(self):
        """
        Tests that user account can be created, verifies:
        - User ID is assigned
        - Field values present in returned object.
        - Password not returned to user.
        """
        payload = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@example.com",
            "password": "password123"
        }

        response = self.client.post('/account', payload, format='json')
        user_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

        del payload["password"]
        for k, v in payload.items():
            self.assertEqual(user_json[k], v, msg=f"User Content\n\n{user_json}")

        self.assertNotIn('password', user_json)

    def test_create_account_invalid_email(self):
        """
        Tests that valid email must be given to user.
        """
        payload = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "invalid-email"
        }

        response = self.client.post('/account', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_account_no_password(self):
        """
        Tests that account cannot be created without password
        """
        payload = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@example.com",
        }

        response = self.client.post('/account', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_update_account_new_password(self):
        """
        Tests that account cannot update the password via the PUT endpoint.
        """
        # Create a new account
        payload = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@example.com",
            "password": "password123"
        }
        creation_response = self.client.post('/account', payload, format='json')
        self.assertEqual(creation_response.status_code, status.HTTP_201_CREATED)

        # Log in to get the JWT token
        login_payload = {
            "email": "johndoe@example.com",
            "password": "password123"
        }
        login_response = self.client.post('/login', login_payload, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access']  # Assuming the token is in 'access'

        # Update account with an attempt to change the password
        account = creation_response.json()
        update_payload = {
            "id": account["id"],
            "password": "new_password"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')  # Set the Authorization header
        update_response = self.client.put('/account', update_payload, format='json')

        # Assertions
        self.assertEqual(update_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', update_response.data)
        password_error = update_response.data['password'][0]
        self.assertIn('Password updates are not allowed via this endpoint', password_error)
