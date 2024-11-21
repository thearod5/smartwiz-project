from rest_framework import status
from rest_framework.test import APITestCase

from utils import create_test_account


class ReturnTest(APITestCase):
    def setUp(self):
        self.user = create_test_account(self.client)

    def test_create_return(self):
        """
        Creates a populated return.
        """
        payload = {"year": 2024}  # minimal return initialization
        response = self.client.post('/return', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['year'], 2024)

    def test_create_return_missing_field(self):
        """
        Tests that payload must contain user and year of return
        """
        response = self.client.post('/return', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

        user_returns = self._get_returns()
        self.assertEqual(len(user_returns), 0)

    def test_no_duplicate_returns(self):
        """
        Tests that users are not allowed to create multiple returns for the same year.
        """
        self._create_return(year=2024)
        response = self._create_return(year=2024, return_response=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.data["non_field_errors"]
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertIn("A return for this year already exists for the user", error)

    def test_update_return(self):
        """
        Tests that user is able to update a return.
        """
        return_json = self._create_return(year=2024)
        return_json["annualIncome"] = 40_000

        updates = {"annualIncome": 40_000, "attendedSchool": True, "ownedHome": True}
        for k, v in updates.items():
            updated_json = self._update_return(id=return_json["id"], **{k: v})
            self.assertEqual(updated_json[k], v)
            returns = self._get_returns()
            self.assertEqual(len(returns), 1)
            return_json = returns[0]
            self.assertEqual(return_json[k], v)

    def _create_return(self, return_response: bool = False, **kwargs):
        """
        Creates return for current user with given kwargs
        :param return_response: Returns the entire HTTP response to request.
        :param kwargs: Kwargs forming payload of POST request.
        :return: Response Json if not response not set otherwise response.
        """
        payload = {"user": str(self.user.id), **kwargs}
        response = self.client.post('/return', payload, format='json')
        if return_response:
            return response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()

    def _update_return(self, **kwargs):
        """
        Updates return formed via kwargs
        :param kwargs: Kwargs forming payload of PUT method.
        :return: Response Json.
        """
        response = self.client.put("/return", kwargs, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()

    def _get_returns(self):
        """
        :return: List of returns associated with current user.
        """
        response = self.client.get("/return", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()
