from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.endpoints.accounts.account_serializer import UserSerializer


class CreateAccountView(APIView):
    def post(self, request):
        """
        Creates new account given a user object.
        :param request:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
