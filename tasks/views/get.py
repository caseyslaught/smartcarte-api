from django.core.exceptions import ValidationError
import json
from rest_framework import permissions, status, generics
from rest_framework.response import Response

from SmartCarteApi.common.authentication import CognitoAuthentication
from tasks.serializers import create as serializer

from tasks.models import ForestChangeTask
from tasks.serializers import get as serializers


class GetForestChangeTaskInfoView(generics.GenericAPIView):

    authentication_classes = [CognitoAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GetForestChangeTaskParamsSerializer

    def get(self, request):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class GetForestChangeTaskParamsView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.GetForestChangeTaskParamsSerializer

    def get(self, request):

        task_uid = request.query_params.get('task_uid')

        try:
            task = ForestChangeTask.objects.get(uid=task_uid)
        except (ForestChangeTask.DoesNotExist, ValidationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            geojson = json.loads(task.region.geojson)
        except json.decoder.JSONDecodeError:
            return Response({'error': 'json_decode_error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({
            'start_date': task.start_date,
            'end_date': task.end_date,
            'region': {
                'name': task.region.name,
                'geojson': geojson
            }
        }, status=status.HTTP_200_OK)


