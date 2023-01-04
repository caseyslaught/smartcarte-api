from rest_framework import serializers

from account.serializers.account import GetRegionSerializer
from tasks.models import ForestChangeTask


class GetForestChangeTaskParamsSerializer(serializers.ModelSerializer):    

    region_geojson = serializers.SerializerMethodField()
    def get_region_geojson(self, task):
        return task.region.geojson

    class Meta:
        model = ForestChangeTask
        fields = [
            'start_date',
            'end_date',
            'region_geojson',
        ]

    