from __future__ import absolute_import

from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction
from django.utils.encoding import python_2_unicode_compatible

from rest_framework_jwt.settings import api_settings

class UserManager(BaseUserManager):

    def generate_token(self, user):
        return api_settings.JWT_ENCODE_HANDLER({
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })

    def get_by_natural_key(self, username):
        return self.get(username = username)

    @transaction.atomic
    def create_user(self, username, password, **kwargs):
        if not kwargs.get('email'):
            raise ValueError('User must have valid email address')

        account = self.model(username = username,
                             email = self.normalize_email(kwargs.get('email', '')))
        account.last_login = datetime.now()
        account.set_password(password)
        account.token = self.generate_token(account)
        account.save(using = self._db)
        return account

    @transaction.atomic
    def create_superuser(self, username, password = None, **kwargs):
        account = self.create_user(username, password, **kwargs)
        account.is_admin = True
        account.save(using = self._db)
        return account



class Company(models.Model):
    name = models.CharField(max_length = 100, unique = True, default = '')
    description = models.CharField(max_length = 255, default = '')
    active = models.BooleanField(default = True)

    class Meta:
        db_table = 'user_company'

    @python_2_unicode_compatible
    def __str__(self):
        return '[Name: {}] [Active: {}]'.format(self.name, self.active)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(unique = True)
    token = models.CharField(max_length = 255, default = '', unique = True)
    company = models.ForeignKey(Company, null = True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def generate_token(self):
        self.token = User.objects.generate_token(user = self)
        self.save()

    @python_2_unicode_compatible
    def __str__(self):
        return '[Username: {}] [Email: {}]'.format(self.username, self.email)





