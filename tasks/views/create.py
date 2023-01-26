from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from account.models import Region
from SmartCarteApi.common.authentication import CognitoAuthentication
from SmartCarteApi.common.aws.ecs import run_fargate_monolith_task
from SmartCarteApi.common.constants import TASK_TYPE_FOREST_CHANGE
from tasks.models import ForestChangeTask
from tasks.serializers import create as serializers


class CreateForestChangeTaskView(generics.GenericAPIView):

    authentication_classes = [CognitoAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CreateForestChangeTaskSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        start_date = data['start_date']
        end_date = data['end_date']
        region_uid = data['region_uid']

        try:
            region = Region.objects.get(uid=region_uid)
        except  Region.DoesNotExist:
            return Response({'error': 'region_not_found'}, status=status.HTTP_400_BAD_REQUEST)

        task = ForestChangeTask.objects.create(
            type=TASK_TYPE_FOREST_CHANGE,
            status='pending',
            account=request.user,
            organization=request.user.organization,
            start_date=start_date,
            end_date=end_date,
            region=region,
        )

        run_fargate_monolith_task(task)

        return Response({'task_uid': task.uid}, status=status.HTTP_201_CREATED)


