from django.db import IntegrityError
from rest_framework import permissions, status, generics, views
from rest_framework.response import Response

from account.models import Account, Organization, Waitlist
from account.serializers import account as serializers
from SmartCarteApi.common.aws import cognito, exceptions


class RegisterView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        email = data['email']
        password = data['password']
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        organization_name = data.get('organization_name', "")

        organization = Organization.objects.create(name=organization_name)

        try:
            uid_cognito = cognito.create_user(email, password, method='email')
            cognito.confirm_account(email)
            account = Account.objects.create(
                uid_cognito=uid_cognito,
                organization=organization,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_admin=True)
        except (IntegrityError, exceptions.UsernameExistsException):
            organization.delete()
            return Response({
                'error': 'email_already_exists',
                'message': 'This email already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)
        except (exceptions.ParamValidationError, exceptions.InvalidParameterException):
            organization.delete()
            return Response({
                'error': 'invalid_parameter',
                'message': 'Invalid parameter.'
                }, status=status.HTTP_400_BAD_REQUEST)

        tokens = cognito.sign_in(email, password)

        return Response({
            'account_uid': account.uid_cognito,
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }, status=status.HTTP_201_CREATED)



class WaitlistSignupView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.WaitlistSignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        Waitlist.objects.create(**data)

        return Response(status=status.HTTP_201_CREATED)

