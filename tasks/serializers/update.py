from rest_framework import serializers

from SmartCarteApi.common.constants import TASK_STATUSES


class UpdateTaskStatusSerializer(serializers.Serializer):
    task_uid = serializers.UUIDField()
    task_type = serializers.CharField()
    status = serializers.ChoiceField(choices=TASK_STATUSES)


class UpdateForestChangeTaskResultsSerializer(serializers.Serializer):
    task_uid = serializers.UUIDField()
    gain_area = serializers.IntegerField()
    loss_area = serializers.IntegerField()
    total_area = serializers.IntegerField() # non-masked area

        