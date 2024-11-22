from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User
from utils import create_test_account


class ChatTest(APITestCase):
    def setUp(self):
        """
        Creates user, address, and sets as primary location.
        """
        self.user = create_test_account(self.client, first_name="Alberto", last_name="Rodriguez")
        self.address = self._create_address(address="111 S. Morgan St., Chicago, IL, 60607")
        account_update_response = self.client.put("/account", {"primaryAddress": self.address["id"]}, format="json")
        self.assertEqual(account_update_response.status_code, status.HTTP_200_OK)
        current_user = User.objects.get(id=self.user.id)
        self.assertIsNotNone(current_user.primary_address)

    def test_chat(self):
        messages = []
        response = self.get_chat_response(messages)
        self.assertIsNone(response["form"])
        messages.append({"type": "assistant", "content": response["response"]})

        messages.append({"type": "user", "content": "I am a software engineer making 40k a year. I rent an apartment."})
        response2 = self.get_chat_response(messages)
        print(response)

    def get_chat_response(self, messages):
        response = self.client.post("/chat", {"messages": messages}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()

    def _create_address(self, **kwargs):
        """
        Creates new address.
        :param kwargs: Kwargs forming payload to address.
        :return: The address json.
        """
        response = self.client.post("/address", kwargs, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()
