from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "phone_number",
            "profile_photo",
            "street",
            "city",
            "state",
            "postal_code",
            "api_token",
            "credit",
            "is_subscribed",
            "is_trial",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"


class UpdateProfileSerializer(serializers.ModelSerializer):
    # country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "city",
            "street",
            "is_subscribed",
            "is_trial",
        ]
