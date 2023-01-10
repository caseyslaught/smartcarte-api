from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from SmartCarteApi.common.authentication import CognitoAuthentication
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

        # 1. create the task in the database
        # 2. start an ECS Fargate task

        return Response(status=status.HTTP_201_CREATED)


