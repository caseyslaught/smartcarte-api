from rest_framework import serializers



class CreateForestChangeTaskSerializer(serializers.Serializer):

    start_date = serializers.DateField()
    end_date = serializers.DateField()
    region_uid = serializers.UUIDField()




    