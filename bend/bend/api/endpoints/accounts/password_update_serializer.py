from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        """Ensure the old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def update(self, instance, validated_data):
        """Update the user's password."""
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
