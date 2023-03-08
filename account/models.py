from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

from SmartCarteApi.common import get_utc_datetime_now
from SmartCarteApi.common.aws import cognito, exceptions


class Organization(models.Model):

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    datetime_created = models.DateTimeField(default=get_utc_datetime_now)
    datetime_updated = models.DateTimeField(null=True)
    datetime_deleted = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True) # set true if deleted

    name = models.CharField(max_length=120, blank=True, default="")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password, **extra_fields):

        try:
            organization = Organization.objects.get(name='Smart Carte')
        except Organization.DoesNotExist:
            organization = Organization.objects.create(name='Smart Carte')

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('organization', organization)

        email = self.normalize_email(email).lower()
        account = self.model(email=email, **extra_fields)

        try:
            uid_cognito = cognito.create_user(email, password, method="superuser")
            cognito.confirm_account(email)
            cognito.verify_email(email)
        except exceptions.UsernameExistsException:
            print("User already exists in Cognito but just added to database.")
            uid_cognito = cognito.get_uid_cognito(email)
        
        account.uid_cognito = uid_cognito
        account.set_password(password)
        account.save(using=self._db)

        return account



class Account(AbstractBaseUser, PermissionsMixin):
    
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    datetime_created = models.DateTimeField(default=get_utc_datetime_now)
    datetime_updated = models.DateTimeField(null=True)
    datetime_deleted = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True) # set true if deleted

    uid_cognito = models.UUIDField(null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)

    is_superuser = models.BooleanField(default=False) # superuser
    is_staff = models.BooleanField(default=False) # superuser
    is_admin = models.BooleanField(default=True) # organization admin

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='accounts')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email
    

class DemoUser(models.Model):

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    datetime_created = models.DateTimeField(default=get_utc_datetime_now)
    datetime_deleted = models.DateTimeField(null=True)

    # tracking ID that is created by frontend and passed to backend
    # not using UUIDField because format may change
    tid = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.tid


class Region(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    datetime_created = models.DateTimeField(default=get_utc_datetime_now)
    datetime_updated = models.DateTimeField(null=True)
    datetime_deleted = models.DateTimeField(null=True)

    name = models.CharField(max_length=200, blank=True, null=True)
    geojson = models.TextField()

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='regions')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='regions')

    def __str__(self):
        return self.name


class Waitlist(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    datetime_created = models.DateTimeField(default=get_utc_datetime_now)

    # if demo_user is not null, then signup if from demo not form
    demo_user = models.ForeignKey(DemoUser, on_delete=models.CASCADE, related_name='waitlist_signups', null=True)

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()

    industry = models.CharField(max_length=100, blank=True, null=True) # conservation, agriculture, mining
    reason = models.CharField(max_length=100, blank=True, null=True) # burn area, lulc, forest
    role = models.CharField(max_length=100, blank=True, null=True) # researcher, press, pa manager
    message = models.TextField(blank=True, null=True)

