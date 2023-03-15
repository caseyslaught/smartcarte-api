from rest_framework import serializers

from SmartCarteApi.common.constants import TASK_STATUSES


class UpdateTaskStatusSerializer(serializers.Serializer):

    task_uid = serializers.UUIDField()
    task_type = serializers.CharField()
    status = serializers.ChoiceField(choices=TASK_STATUSES)
    message = serializers.CharField(required=False, allow_null=True) # allow_null makes serializer output default None if not specified
    long_message = serializers.CharField(required=False, allow_null=True) 

    def validate(self, attrs):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError(f'Unknown field(s): {", ".join(unknown)}')
        return attrs


class UpdateDemoTaskSerializer(serializers.Serializer):

    task_uid = serializers.UUIDField()
    statistics_json = serializers.JSONField(required=False)
    imagery_tif_href = serializers.URLField(required=False)
    imagery_tiles_href = serializers.URLField(required=False)
    landcover_tif_href = serializers.URLField(required=False)
    landcover_tiles_href = serializers.URLField(required=False)

    def validate(self, attrs):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError(f'Unknown field(s): {", ".join(unknown)}')
        return attrs


class UpdateForestChangeTaskSerializer(serializers.Serializer):

    task_uid = serializers.UUIDField()

    gain_area = serializers.IntegerField(required=False)
    loss_area = serializers.IntegerField(required=False)
    total_area = serializers.IntegerField(required=False) # non-masked area

    before_rgb_tiles_href = serializers.URLField(required=False)
    after_rgb_tiles_href = serializers.URLField(required=False)
    change_tiles_href = serializers.URLField(required=False)

    def validate(self, attrs):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError(f'Unknown field(s): {", ".join(unknown)}')
        return attrs

