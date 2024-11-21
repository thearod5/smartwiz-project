from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Address


class DeleteAddressView(APIView):
    def delete(self, request, address_id):
        user = request.user
        try:
            address = Address.objects.get(id=address_id, user=user)
            address.delete()
            return Response({'message': 'Address deleted successfully.'}, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
