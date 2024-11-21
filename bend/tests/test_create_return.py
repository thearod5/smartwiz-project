from rest_framework import status
from rest_framework.test import APITestCase

from app.models import User


class CreateReturnTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="John Doe",
            email="johndoe@example.com"
        )

    def test_create_return(self):
        """
        Creates a populated return.
        """
        payload = {
            "user": str(self.user.id),
            "year": 2024,
            "annual_income": 75000,
            "attended_school": True,
            "owned_home": False
        }

        response = self.client.post('/return', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['year'], 2024)
        self.assertEqual(response.data['annual_income'], 75000)

    def test_create_return_missing_field(self):
        """
        Tests that payload must contain user and year of return
        """
        payload = {
            "user": str(self.user.id),
            # "year": 2024 <- missing year
        }

        response = self.client.post('/return', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

    def test_no_duplicate_returns(self):
        """
        Tests that users are not allowed to create multiple returns for the same year.
        """
        payload = {
            "user": str(self.user.id),
            "year": 2024
        }

        response = self.client.post('/return', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to create another return
        response = self.client.post('/return', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.data["non_field_errors"]
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertIn("unique set", error)
