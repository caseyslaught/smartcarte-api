from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

from SmartCarteApi.common import get_utc_datetime_now
from SmartCarteApi.common.aws import cognito


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

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
    full_name = models.CharField(max_length=200, blank=True, null=True)

    is_superuser = models.BooleanField(default=False) # superuser
    is_staff = models.BooleanField(default=False) # superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['email']

    def __str__(self):
        return f'{self.email} - {self.full_name}'
