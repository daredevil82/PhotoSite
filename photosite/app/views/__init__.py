from __future__ import absolute_import
import logging

from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response

class AbstractView(views.APIView):
    def __init__(self):
        self.log = logging.getLogger('django')

    def error_response(self, msg, status = status.HTTP_404_NOT_FOUND):
        return Response({'msg': msg}, status)
