from rest_framework import status
from rest_framework.test import APITestCase


class CreateAccountTest(APITestCase):
    def test_create_account(self):
        payload = {
            "name": "John Doe",
            "email": "johndoe@example.com"
        }

        response = self.client.post('/account', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], "John Doe")
        self.assertEqual(response.data['email'], "johndoe@example.com")

    def test_create_account_invalid_email(self):
        payload = {
            "name": "John Doe",
            "email": "invalid-email"
        }

        response = self.client.post('/account', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
