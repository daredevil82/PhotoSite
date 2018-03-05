from __future__ import absolute_import


from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage

from photosite.settings import settings

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION