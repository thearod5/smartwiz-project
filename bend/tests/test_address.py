from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User
from utils import create_test_account


class AddressTest(APITestCase):
    address_str = "111 S. Morgan St., Chicago, IL, 60607"
    expected = {"street": "111 S. Morgan St.", "city": "Chicago", "state": "IL", "zipCode": "60607"}

    def setUp(self):
        self.user = create_test_account(self.client)

    def test_create_new_address(self):
        """
        Tests that a new address can be created.
        """
        address_json = self._create_address(address=self.address_str)
        for k, v in self.expected.items():
            self.assertEqual(address_json[k], v)

        addresses = self._get_addresses()
        self.assertEqual(len(addresses), 1)
        address = addresses[0]
        for k, v in self.expected.items():
            self.assertEqual(address[k], v, msg=f"{k} received ({address[k]}) not equal to {v}")

    def test_primary_address(self):
        """
        Tests that address can be set as primary address for user.
        """
        address_json = self._create_address(address=self.address_str)
        update_response = self.client.put("/account", {"primaryAddress": address_json['id']}, format="json")
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        user_object = User.objects.get(id=self.user.id)
        address_object = user_object.primary_address
        for k, v in self.expected.items():
            if k == "zipCode":
                k = "zip_code"  # TODO: Generalize this later...
            self.assertEqual(getattr(address_object, k), v)

    def test_delete_address(self):
        """
        Tests that address can be created and deleted.
        """
        address_json = self._create_address(address=self.address_str)
        delete_response = self.client.delete(f"/address/{address_json['id']}")
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        addresses = self._get_addresses()
        self.assertEqual(len(addresses), 0)

    def _create_address(self, **kwargs):
        """
        Creates new address.
        :param kwargs: Kwargs forming payload to address.
        :return: The address json.
        """
        response = self.client.post("/address", kwargs, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()

    def _get_addresses(self):
        """
        :return: Returns list of addresses associated with user.
        """
        get_response = self.client.get("/address", format="json")
        return get_response.json()
