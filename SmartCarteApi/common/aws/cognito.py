from botocore.exceptions import ClientError, ParamValidationError
from django.conf import settings

from SmartCarteApi.common.aws import exceptions, get_boto_client


def confirm_account(email):

    client = get_boto_client('cognito-idp')

    client.admin_confirm_sign_up(
        UserPoolId=settings.COGNITO_USERPOOL_ID,
        Username=email
    )


def create_user(email, password, method="email"):

    client = get_boto_client('cognito-idp')

    try:
        response = client.sign_up(
            ClientId=settings.COGNITO_APP_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': 'registration_method',
                    'Value': method
                },
            ]
        )
    except ParamValidationError:
        raise exceptions.ParamValidationError
    except client.exceptions.InvalidParameterException:
        raise exceptions.InvalidParameterException
    except client.exceptions.UsernameExistsException:
        raise exceptions.UsernameExistsException
    else:
        return response['UserSub']


def forgot_password(email):

    client = get_boto_client('cognito-idp')

    try:
        client.forgot_password(
            ClientId=settings.COGNITO_APP_ID,
            Username=email
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException
    except client.exceptions.InvalidParameterException:
        raise exceptions.InvalidParameterException
    except client.exceptions.LimitExceededException:
        raise exceptions.LimitExceededException
    except client.exceptions.UserNotFoundException:
        raise exceptions.UserNotFoundException


def forgot_password_confirm(email, code, password):

    client = get_boto_client('cognito-idp')

    try:
        client.confirm_forgot_password(
            ClientId=settings.COGNITO_APP_ID,
            Username=email,
            ConfirmationCode=code,
            Password=password
        )
    except client.exceptions.CodeMismatchException:
        raise exceptions.CodeMismatchException
    except client.exceptions.ExpiredCodeException:
        raise exceptions.ExpiredCodeException
    except client.exceptions.UserNotFoundException:
        raise exceptions.UserNotFoundException
    except ParamValidationError:
        raise exceptions.ParamValidationError


def get_is_email_verified(email):
    
    client = get_boto_client('cognito-idp')
    cognito_response = client.admin_get_user(
        UserPoolId=settings.COGNITO_USERPOOL_ID,
        Username=email
    )

    is_email_verified = False
    for attr in cognito_response['UserAttributes']:
        if attr['Name'] == 'email_verified':
            is_email_verified = attr['Value'] == 'true'

    return is_email_verified


def refresh(refresh_token):

    client = get_boto_client('cognito-idp')

    try:
        response = client.initiate_auth(
            ClientId=settings.COGNITO_APP_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
            }
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException

    return response['AuthenticationResult']['AccessToken']


def sign_in(email, password):

    client = get_boto_client('cognito-idp')

    try:
        response = client.admin_initiate_auth(
            UserPoolId=settings.COGNITO_USERPOOL_ID,
            ClientId=settings.COGNITO_APP_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH', # must configure app client
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException
    except client.exceptions.UserNotConfirmedException:
        raise exceptions.UserNotConfirmedException
    except client.exceptions.UserNotFoundException:
        raise exceptions.UserNotFoundException

    # check if password change required
    if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
        raise exceptions.NewPasswordRequiredError

    return {
        'access_token': response['AuthenticationResult']['AccessToken'],
        'refresh_token': response['AuthenticationResult']['RefreshToken']
    }


def sign_out(email):

    client = get_boto_client('cognito-idp')
    client.admin_user_global_sign_out(
        UserPoolId=settings.COGNITO_USERPOOL_ID,
        Username=email
    )


def verify_email(email):
    
    client = get_boto_client('cognito-idp')
    client.admin_update_user_attributes(
        UserPoolId=settings.COGNITO_USERPOOL_ID,
        Username=email,
        UserAttributes=[
            {
                'Name': 'email_verified',
                'Value': 'true'
            },
        ]
    )

