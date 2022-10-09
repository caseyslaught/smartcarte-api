from django.conf import settings
from django.utils.encoding import smart_str
import json
import jwt
import os
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication, get_authorization_header
import time

from account.models import Account
from SmartCarteApi.common.aws import get_boto_client


class CognitoAuthentication(BaseAuthentication):

    def authenticate(self, request):

        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        self.verify_cognito_token_valid(jwt_value)
        self.verify_cognito_kid(jwt_value)

        # verify uid or username exists (both same in Cognito)

        # must use PyJWT==1.7.1
        unverified_payload = jwt.decode(jwt_value, None, False)
        uid = unverified_payload.get('sub', unverified_payload.get('username', None))
        if uid is None:
            raise exceptions.AuthenticationFailed({
                'error': 'sub_claim_required'
            })

        self.verify_expiry(unverified_payload)

        try:
            account = Account.objects.get(uid_cognito=uid)
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed({
                'error': 'no_user_with_sub'
            })

        return account, jwt_value


    # this cannot be static
    def get_jwt_value(self, request):

        auth = get_authorization_header(request).split()
        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            raise exceptions.AuthenticationFailed({
                'error': 'no_auth_header'
            })

        if smart_str(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed({
                'error': 'invalid_auth_header_no_creds'
            })

        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed({
                'error': 'invalid_auth_header_spaces'
            })

        return auth[1]


    def verify_cognito_token_valid(self, jwt_value):

        # verify that access_token is still valid
        boto3_client = get_boto_client('cognito-idp')
        try:
            boto3_client.get_user(AccessToken=jwt_value.decode('utf-8'))

        except boto3_client.exceptions.NotAuthorizedException:
            raise exceptions.AuthenticationFailed({
                'error': 'access_token_revoked'
            })

        except boto3_client.exceptions.UserNotFoundException as unfe:
            raise exceptions.AuthenticationFailed({
                'error': 'user_not_found'
            })

        except boto3_client.exceptions.ResourceNotFoundException as rnfe:
            raise exceptions.AuthenticationFailed({
                'error': 'resource_not_found'
            })


    def verify_expiry(self, payload):

        expiry_secs = payload.get('exp')
        if expiry_secs is None:
            raise exceptions.AuthenticationFailed({
                'error': 'no_exp_in_access_token'
            })
        elif expiry_secs < int(round(time.time())):
            raise exceptions.AuthenticationFailed({
                'error': 'access_token_expired'
            }, status.HTTP_403_FORBIDDEN)


    def verify_cognito_kid(self, jwt_value):
        """
        Verifies that the kid in the access_token header matches a well-known kid in Cognito
        """

        try:
            jwt_kid = jwt.get_unverified_header(jwt_value).get('kid')
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed({
                'error': 'invalid_jwt'
            })

        if jwt_kid is None:
            raise exceptions.AuthenticationFailed({
                'error': 'kid_required'
            })

        jwk_path  = os.path.join(settings.BASE_DIR, 'account', 'resources', 'jwks.json')

        if not os.path.isfile(jwk_path):
            raise exceptions.AuthenticationFailed({
                'error': 'jwks_missing'
            })

        with open(jwk_path) as f:
            keys = [key['kid'] for key in json.loads(f.read())['keys']]

        if not jwt_kid in keys:
            raise exceptions.AuthenticationFailed({
                'error': 'invalid_kid'
            })

            
