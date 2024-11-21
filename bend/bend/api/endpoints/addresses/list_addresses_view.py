from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.endpoints.addresses.address_serializer import AddressSerializer
from api.models import Address


class ListUserAddressesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
