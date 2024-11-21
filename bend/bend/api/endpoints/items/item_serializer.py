from rest_framework import serializers

from api.models import Return
from api.models.item import Item


class ItemSerializer(serializers.ModelSerializer):
    return_record = serializers.CharField(write_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'return_record',
            'type',
            'name',
            'description',
            'amount'
        ]

    def create(self, validated_data):
        # Convert the return_record UUID into a Return instance
        return_record_id = validated_data.pop('return_record')
        return_record = Return.objects.get(id=return_record_id)  # Ensure the instance exists
        validated_data['return_record'] = return_record

        # Create the Item instance
        return super().create(validated_data)
