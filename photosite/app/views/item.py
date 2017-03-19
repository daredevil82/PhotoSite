from __future__ import absolute_import

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from app.models.user import Company, User
from app.models.content import Image, UploadItem
from app.views import AbstractView

class UploadItemView(AbstractView):
    def __init__(self):
        super().__init__()

