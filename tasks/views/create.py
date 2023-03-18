from datetime import datetime as dt
from dateutil import parser
from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from account.models import DemoUser, Region, Waitlist
from SmartCarteApi.common.authentication import CognitoAuthentication
from SmartCarteApi.common.aws.ecs import run_fargate_monolith_task
from SmartCarteApi.common.constants import TASK_TYPE_FOREST_CHANGE
from tasks.models import DemoLandcoverClassificationTask, ForestChangeTask
from tasks.serializers import create as serializers


class CreateDemoClassificationTaskView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CreateDemoClassificationTaskSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        date = parser.parse(data['date'])
        region_geojson = data['region_geojson']
        email = data['email']
        add_to_waitlist = data['add_to_waitlist']
        tid = data['tid']

        print(data)            

        if date < parser.parse('2019-01-01'):
            return Response({
                'error': 'invalid_date', 
                'message': 'imagery is available from January 2019'}, 
                status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: validate geojson?

        try:
            demo_user = DemoUser.objects.get(tid=tid)
        except DemoUser.DoesNotExist:
            demo_user = DemoUser.objects.create(tid=tid)

        """
        old_tasks = DemoLandcoverClassificationTask.objects.filter(demo_user=demo_user, status__in=['pending', 'running'])            
        if len(old_tasks) > 0:
            return Response({
                'error': 'task_limit', 
                'message': 'You can only have one running task at a time. Please wait for the other one to finish before starting a new one.',
                'current_task_uids': [t.uid for t in old_tasks]
            }, status=status.HTTP_400_BAD_REQUEST)
        """

        # only add to waitlist if demo user hasn't already added this email
        if add_to_waitlist:
            try:
                Waitlist.objects.get(email=email, demo_user=demo_user)
                print('not adding duplicate waitlister')
            except Waitlist.DoesNotExist:
                Waitlist.objects.create(email=email, demo_user=demo_user)

        task = DemoLandcoverClassificationTask.objects.create(
            type="demo_classification",
            status="pending",
            status_message="Starting task",
            date=date,
            email=email,
            region_geojson=region_geojson,
            demo_user=demo_user,
            statistics_json=""
        )

        fargate_res = run_fargate_monolith_task(task)

        if len(fargate_res['failures']) > 0:
            task.delete()
            return Response({
                'error': 'fargate_error', 
                'message': 'Our servers have reached capacity. Please try again later.',
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'task_uid': task.uid}, status=status.HTTP_201_CREATED)



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


