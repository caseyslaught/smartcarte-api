from rest_framework import serializers



class CreateDemoClassificationTaskSerializer(serializers.Serializer):

    date = serializers.DateField()
    region_geojson = serializers.CharField()
    email = serializers.EmailField(required=False)
    add_to_waitlist = serializers.BooleanField(default=False)
    tid = serializers.UUIDField()


class CreateForestChangeTaskSerializer(serializers.Serializer):

    start_date = serializers.DateField()
    end_date = serializers.DateField()
    region_uid = serializers.UUIDField()




    