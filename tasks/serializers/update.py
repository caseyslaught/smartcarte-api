from rest_framework import serializers


class UpdateTaskStatusSerializer(serializers.Serializer):
    task_uid = serializers.UUIDField()
    task_type = serializers.CharField()
    status = serializers.CharField()
