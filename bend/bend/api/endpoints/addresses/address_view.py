from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.endpoints.addresses.address_serializer import AddressSerializer
from api.models import Address


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        address_string = request.data.get('address')
        if not address_string:
            return Response({'error': 'Address string is required.'}, status=status.HTTP_400_BAD_REQUEST)

        address_parts = address_string.split(",")
        if len(address_parts) != 4:
            raise ValueError("Invalid address format. Expected [street, city, state, postal_code]")

        # TODO: Need to better validate inputs
        new_address = Address.objects.create(
            user=user,
            display=address_string,
            street=address_parts[0].strip(),
            city=address_parts[1].strip(),
            state=address_parts[2].strip(),
            zip_code=address_parts[3].strip()
        )

        # Serialize the newly created Address object
        serializer = AddressSerializer(instance=new_address)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Retrieves list of addresses for authenticated user.
        :param request: The HTTP request.
        :return: List of addresses
        """
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, address_id):
        """
        Deletes a specific address for the authenticated user.
        :param request: The HTTP request.
        :param address_id: The ID of the address to delete.
        :return: A success message or error response.
        """
        try:
            # Retrieve the address, ensuring it belongs to the authenticated user
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user owns the address
        if address.user != request.user:
            raise PermissionDenied("You do not have permission to delete this address.")

        # Delete the address
        address.delete()
        return Response({'message': 'Address deleted successfully.'}, status=status.HTTP_200_OK)
