from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "id",
            "phone_number",
            "profile_photo",
            "city",
            "state",
            "postal_code",
            "api_token",
            "is_subscribed",
            "is_trial",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    # country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "city",
            "is_subscribed",
            "is_trial",
        ]
