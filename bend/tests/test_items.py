from rest_framework import status
from rest_framework.test import APITestCase

from utils import create_test_account


class ItemTest(APITestCase):
    def setUp(self):
        self.user = create_test_account(self.client)
        self.tax_return = self.client.post('/return', {"year": 2024}, format='json').json()

    def test_create_item(self):
        """
        Tests that user is able to create an itemization.
        """
        self.assertEqual(len(self._get_items()), 0)
        payload = {"name": "Attending School", "type": "deduction", "amount": 1800}
        item_json = self._create_item(**payload)
        for k, v in payload.items():
            self.assertEqual(item_json[k], v)
        self.assertEqual(len(self._get_items()), 1)

    def test_update_item(self):
        """
        Tests that user is able to update item.
        :return:
        """
        payload = {"name": "Attending School", "type": "deduction", "amount": 1800}
        item_json = self._create_item(**payload)

        item_updates = {"name": "New Name", "type": "credit", "amount": 3600}
        for k, v in item_updates.items():
            update_response = self.client.put("/item", {"id": item_json["id"], k: v}, format='json')
            self.assertEqual(update_response.status_code, status.HTTP_200_OK)
            return_items = self._get_items()
            self.assertEqual(len(return_items), 1)
            item = return_items[0]
            self.assertEqual(item[k], v)

    def test_delete_item(self):
        """
        Tests that user is able to delete item.
        """
        payload = {"name": "Attending School", "type": "deduction", "amount": 1800}
        item_json = self._create_item(**payload)

        delete_response = self.client.delete(f"/item/{item_json['id']}", {"amount": 3600}, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(self._get_items()), 0)

    def _create_item(self, **kwargs):
        """
        Creates item for return
        :param kwargs: Kwargs forming payload to POST request.
        :return: Json of item created
        """
        kwargs["return_record"] = self.tax_return["id"]
        create_response = self.client.post("/item", kwargs, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        return create_response.json()

    def _get_items(self):
        """
        Gets items for current return.
        :return: List of items in return.
        """
        get_response = self.client.get(f"/item/return/{self.tax_return['id']}")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        return get_response.json()
