import json
from rest_framework import permissions, status, generics
from rest_framework.response import Response

from SmartCarteApi.common import  get_utc_datetime_now
from SmartCarteApi.common.constants import TASK_STATUS_CANCELED, TASK_STATUS_COMPLETE, TASK_STATUS_FAILED
from tasks.models import DemoLandcoverClassificationTask, ForestChangeTask
from tasks.serializers import update as serializers


class UpdateDemoClassificationTaskView(generics.GenericAPIView):
    """
    View for updating just demo classification change tasks.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UpdateDemoTaskSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        task_uid = data['task_uid']

        try:
            task = DemoLandcoverClassificationTask.objects.get(uid=task_uid)
        except DemoLandcoverClassificationTask.DoesNotExist:
            return Response({'error': 'task_not_found'}, status=status.HTTP_400_BAD_REQUEST)
        
        statistics_json = data.get('statistics_json', task.statistics_json)
        statistics_json = json.dumps(statistics_json)

        task.statistics_json = statistics_json
        task.imagery_tif_href = data.get('imagery_tif_href', task.imagery_tif_href)
        task.imagery_tiles_href = data.get('imagery_tiles_href', task.imagery_tiles_href)
        task.landcover_tif_href = data.get('landcover_tif_href', task.landcover_tif_href)
        task.landcover_tiles_href = data.get('landcover_tiles_href', task.landcover_tiles_href)
        task.rgb_tif_href = data.get('rgb_tif_href', task.rgb_tif_href)
        task.save()

        return Response(status=status.HTTP_200_OK)


class UpdateForestChangeTaskView(generics.GenericAPIView):
    """
    View for updating just forest change tasks.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UpdateForestChangeTaskSerializer

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
        task.total_area = data.get('total_area', task.total_area)
        task.gain_area = data.get('gain_area', task.gain_area)
        task.loss_area = data.get('loss_area', task.loss_area)
        task.before_rgb_tiles_href = data.get('before_rgb_tiles_href', task.before_rgb_tiles_href)
        task.after_rgb_tiles_href = data.get('after_rgb_tiles_href', task.after_rgb_tiles_href)
        task.change_tiles_href = data.get('change_tiles_href', task.change_tiles_href)
        task.save()

        return Response(status=status.HTTP_200_OK)


class UpdateTaskStatusView(generics.GenericAPIView):
    """
    View for updating the status of all types of tasks.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UpdateTaskStatusSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        task_uid = data['task_uid']
        task_type = data['task_type']
        task_status = data['status']

        if task_type == "demo_classification":
            TaskClass = DemoLandcoverClassificationTask
        elif task_type == "forest_change":
            TaskClass = ForestChangeTask
        else:
            return Response({'error': 'unknown_task_type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = TaskClass.objects.get(uid=task_uid)
        except TaskClass.DoesNotExist:
            return Response({'error': 'task_not_found'}, status=status.HTTP_400_BAD_REQUEST)

        if task_status in [TASK_STATUS_COMPLETE, TASK_STATUS_CANCELED, TASK_STATUS_FAILED]:
            task.datetime_completed = get_utc_datetime_now()

        task.datetime_updated = get_utc_datetime_now()
        task.status = task_status
        task.status_message = data.get('message')
        task.status_long_message = data.get('long_message')
        task.save()

        return Response(status=status.HTTP_200_OK)

