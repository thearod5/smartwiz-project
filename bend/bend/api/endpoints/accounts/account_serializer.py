from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # Required for creation only

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name', 'primary_address', 'password']

    def validate(self, attrs):
        # Prevent password updates
        if self.instance and 'password' in attrs:
            raise serializers.ValidationError({'password': "Password updates are not allowed via this endpoint."})

        # Check for email uniqueness only if it is being updated
        new_email = attrs.get('email', None)
        if self.instance and new_email and self.instance.email != new_email:
            if User.objects.filter(email=new_email).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({"email": "This email is already in use."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_active = True  # Ensure the account is active
        user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        # Exclude 'password' from being updated via this serializer
        validated_data.pop('password', None)

        # Apply updates to the user instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
