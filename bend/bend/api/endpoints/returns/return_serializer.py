from rest_framework import serializers

from api.models import Return


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'
