from rest_framework import serializers

from api.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class SetPrimaryAddressSerializer(serializers.Serializer):
    address_id = serializers.UUIDField()
