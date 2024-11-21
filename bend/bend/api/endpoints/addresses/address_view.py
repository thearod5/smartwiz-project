from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Address


class CreateAddressView(APIView):
    def post(self, request):
        user = request.user
        address_string = request.data.get('address')
        if not address_string:
            return Response({'error': 'Address string is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Simulating address parsing logic
        # Replace with proper geocoding or address parsing logic
        try:
            address_parts = address_string.split(",")
            if len(address_parts) < 4:
                raise ValueError("Invalid address format.")

            new_address = Address.objects.create(
                user=user,
                display=address_string,
                street_no=address_parts[0].strip(),
                street=address_parts[1].strip(),
                city=address_parts[2].strip(),
                state=address_parts[3].strip(),
                zip_code=address_parts[4].strip() if len(address_parts) > 4 else None
            )
            # TODO: Could use LLM or API to validate the address actually exists / is valid.
            return Response({'message': 'Address created successfully.', 'id': str(new_address.id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
