from rest_framework import permissions, status, generics, views
from rest_framework.response import Response


from account.models import Account
from account.serializers import tokens as serializers
from SmartCarteApi.common.aws import cognito, exceptions
from SmartCarteApi.common.authentication import CognitoAuthentication


class LoginView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email'].lower()
        password = serializer.data['password']

        try:
            Account.objects.get(email=email, is_active=True)
            tokens = cognito.sign_in(email, password)

        except (Account.DoesNotExist, exceptions.NotAuthorizedException, exceptions.UserNotFoundException):
            return Response({
                'error': 'invalid_credentials',
                'message': 'incorrect email and password combination'
                }, status=status.HTTP_403_FORBIDDEN)

        except exceptions.NewPasswordRequiredError:
            return Response({
                'error': 'password_change_required',
                'message': 'use forced password reset flow'
            }, status=status.HTTP_403_FORBIDDEN)

        except exceptions.UserNotConfirmedException:
            return Response({ 
                'error': 'account_not_confirmed',
                'message': 'please verify your email before logging in'
            }, status=status.HTTP_403_FORBIDDEN)

        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(views.APIView):

    authentication_classes = [CognitoAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cognito.sign_out(request.user.email)
        return Response(status=status.HTTP_200_OK)


class RefreshView(generics.GenericAPIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RefreshSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            access_token = cognito.refresh(serializer.data['refresh_token'])
        except exceptions.NotAuthorizedException:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response({
            'access_token': access_token,
        }, status=status.HTTP_200_OK)

