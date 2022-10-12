from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

from SmartCarteApi.common import get_utc_datetime_now
from SmartCarteApi.common.aws import cognito


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

        uid_cognito = cognito.create_user(email, password, method="superuser")
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
