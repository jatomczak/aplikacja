from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    coordinator_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name



class ClientManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Użytkownik musi posiadać adres email.')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(max_length=100, default=None, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    objects = ClientManager()
