from rest_framework import serializers


class SubmitReturnSerializer(serializers.Serializer):
    return_id = serializers.UUIDField()
