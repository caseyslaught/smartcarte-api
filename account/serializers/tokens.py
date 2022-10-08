from rest_framework import serializers

from SmartCarteApi.common.fields import CaseInsensitiveEmailField


class LoginSerializer(serializers.Serializer):

    email = CaseInsensitiveEmailField(required=True, max_length=200)
    password = serializers.CharField(required=True, min_length=7, max_length=50)


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

