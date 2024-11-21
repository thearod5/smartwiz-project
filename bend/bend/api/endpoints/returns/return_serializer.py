from rest_framework import serializers

from api.models import Return


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['id', 'year', 'annual_income', 'attended_school', 'owned_home']  # Exclude 'user'
        read_only_fields = ["id"]

    def validate(self, attrs):
        """
        Validate that the combination of user and year is unique.
        """
        user = self.context['request'].user
        year = attrs.get('year')

        # Check for an existing Return with the same user and year
        if Return.objects.filter(user=user, year=year).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["A return for this year already exists for the user."]}
            )
        return attrs

    def create(self, validated_data):
        """
        Override create to associate the Return with the authenticated user.
        """
        validated_data['user'] = self.context['request'].user  # Automatically set user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override update to ensure the user cannot be changed.
        """
        validated_data['user'] = self.context['request'].user  # Ensure user matches the authenticated user
        return super().update(instance, validated_data)
