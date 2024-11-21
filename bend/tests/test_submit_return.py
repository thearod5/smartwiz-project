import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Return
from utils import create_test_account


class SubmitReturnTest(APITestCase):
    def setUp(self):
        self.user = create_test_account(self.client)
        self.tax_return = Return.objects.create(
            user=self.user,
            year=2024,
            annual_income=75000,
            attended_school=True,
            owned_home=False
        )

    def test_submit_return(self):
        payload = {
            "return_id": str(self.tax_return.id)
        }

        response = self.client.post('/submit', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tax_return.refresh_from_db()
        self.assertIsNotNone(self.tax_return.taxable_income)
        self.assertIn("Return submitted successfully", response.data['message'])

    def test_submit_return_not_found(self):
        payload = {
            "return_id": str(uuid.uuid4())
        }

        response = self.client.post('/submit', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
