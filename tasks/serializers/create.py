from rest_framework import serializers


class CreateForestChangeTaskSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    region_uid = serializers.UUIDField()




    