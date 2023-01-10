from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from SmartCarteApi.common import constants, get_utc_datetime_now
from SmartCarteApi.common.authentication import CognitoAuthentication
from SmartCarteApi.common.constants import TASK_STATUS_CANCELED, TASK_STATUS_COMPLETE, TASK_STATUS_FAILED
from tasks.models import ForestChangeTask
from tasks.serializers import update as serializers



class UpdateForestChangeTaskResultsView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UpdateForestChangeTaskResultsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        task_uid = data['task_uid']

        try:
            task = ForestChangeTask.objects.get(uid=task_uid)
        except ForestChangeTask.DoesNotExist:
            return Response({'error': 'task_not_found'}, status=status.HTTP_400_BAD_REQUEST)

        task.datetime_updated = get_utc_datetime_now()
        task.total_area = data['total_area']
        task.gain_area = data['gain_area']
        task.loss_area = data['loss_area']
        task.save()

        return Response(status=status.HTTP_200_OK)


class UpdateTaskStatusView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UpdateTaskStatusSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        task_uid = data['task_uid']
        task_type = data['task_type']
        new_task_status = data['status']

        if task_type == "forest_change":
            TaskClass = ForestChangeTask
        else:
            return Response({'error': 'unknown_task_type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = TaskClass.objects.get(uid=task_uid)
        except TaskClass.DoesNotExist:
            return Response({'error': 'task_not_found'}, status=status.HTTP_400_BAD_REQUEST)

        if new_task_status in [TASK_STATUS_COMPLETE, TASK_STATUS_CANCELED, TASK_STATUS_FAILED]:
            task.datetime_completed = get_utc_datetime_now()

        task.datetime_updated = get_utc_datetime_now()
        task.status = new_task_status
        task.save()

        return Response(status=status.HTTP_200_OK)


