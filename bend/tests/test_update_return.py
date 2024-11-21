import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from utils import create_test_account


class UpdateReturnTest(APITestCase):
    def setUp(self):
        self.user = create_test_account(self.client)

    def test_update_return(self):
        payload = {
            "user": str(self.user.id),
            "year": 2024
        }

        # Create Initial Return
        return_response = self.client.post("/return", payload, format="json")
        current_return = return_response.json()
        null_fields = ["annualIncome", "taxableIncome", "taxesOwed", "taxesRefunded", "attendedSchool", "ownedHome"]
        for null_field in null_fields:
            self.assertIn(null_field, current_return, msg=f"Current Return\n\n{current_return}")
            self.assertIsNone(current_return[null_field])

        # Update Return
        current_return["annualIncome"] = 40_000
        current_return["attendedSchool"] = True
        current_return["ownedHome"] = True

        # Verify Updates
        response = self.client.put(f'/return/{current_return["id"]}', current_return, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['annual_income'], 40_000)
        self.assertTrue(response.data['attended_school'])
        self.assertTrue(response.data['owned_home'])

    def test_update_return_not_found(self):
        payload = {
            "annual_income": 80000,
            "attended_school": False
        }

        fake_id = uuid.uuid4()
        response = self.client.put(f'/return/{fake_id}', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
