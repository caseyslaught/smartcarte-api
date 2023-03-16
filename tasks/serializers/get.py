import json
from rest_framework import serializers

from tasks.models import DemoLandcoverClassificationTask, ForestChangeTask


class GetDemoClassificationTaskSerializer(serializers.ModelSerializer):

    region_geojson = serializers.SerializerMethodField()
    def get_region_geojson(self, task):
        return json.loads(task.region_geojson)

    class Meta:
        model = DemoLandcoverClassificationTask
        lookup_field = 'uid'
        fields = [
            'uid',
            'datetime_created',
            'date',
            'email',
            'region_geojson',
            'type',
            'status',
            'status_message',
            'status_long_message',
            'statistics_json',
            'imagery_tif_href',
            'imagery_tiles_href',
            'landcover_tif_href',
            'landcover_tiles_href',
            'rgb_tif_href',
        ]


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

    