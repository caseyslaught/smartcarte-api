
from rest_framework import serializers

from SmartCarteApi.common.fields import CaseInsensitiveEmailField
from account.models import Region



class RegisterSerializer(serializers.Serializer):

    email = CaseInsensitiveEmailField(max_length=200)
    password = serializers.CharField(min_length=7, max_length=50)

    organization_name = serializers.CharField(max_length=120, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)



class GetRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = [
            'uid',
            'name',
            'geojson'
        ]