from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.accounts.account_serializer import AccountSerializer


class AccountView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]  # No authentication required for POST
        return [IsAuthenticated()]  # Authentication required for PUT and other methods

    def post(self, request):
        """
        Creates new account given a user object.
        :param request:
        :return:
        """
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        serializer = AccountSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
