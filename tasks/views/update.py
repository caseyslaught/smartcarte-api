from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from SmartCarteApi.common.authentication import CognitoAuthentication
from tasks.models import ForestChangeTask
from tasks.serializers import update as serializers



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
        new_status = data['status']

        if task_type == "forest_change":
            TaskClass = ForestChangeTask
        else:
            return Response({'error': 'unknown_task_type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = TaskClass.objects.get(uid=task_uid)
        except TaskClass.DoesNotExist:
            return Response({'error': 'task_not_found'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()

        return Response(status=status.HTTP_200_OK)


