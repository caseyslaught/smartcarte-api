
from rest_framework import serializers

from SmartCarteApi.common.fields import CaseInsensitiveEmailField



class RegisterSerializer(serializers.Serializer):

    email = CaseInsensitiveEmailField(max_length=200)
    password = serializers.CharField(min_length=7, max_length=50)

    organization_name = serializers.CharField(max_length=120)
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)

