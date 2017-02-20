from __future__ import absolute_import

import logging

from jwt.exceptions import DecodeError
from rest_framework import permissions
from rest_framework_jwt.utils import jwt_decode_handler

from app.models.user import User

class BasePermission(permissions.BasePermission):
    def __init__(self):
        self.logger = logging.getLogger('django')

    def validate_group(self, group_name = '', token = ''):
        self.logger.debug('Validation token for group [%s]', group_name)
        try:
            user = User.objects.get(token = token)
            if user.company is None:
                self.logger.error("User has no company reference, aborting")
                return False
            else:
                if user.company.name.lower() == 'allgroup' or user.company.name.lower() == 'admin':
                    return True
                elif user.company.name.lower() == group_name.lower():
                    return True
                else:
                    self.logger.error('User company does not match company name')
                    return False


        except User.DoesNotExist as e:
            self.logger.exception("User for provided token doesn't exist", e)
            return False


class IsValidToken(BasePermission):
    def __init__(self):
        super().__init__()

    def has_permission(self, request, view):
        if request.auth:
            try:
                jwt_decode_handler(request.auth)
                self.logger.debug('Valid token received')
                return True
            except DecodeError as e:
                self.logger.error('Invalid token received', e)
                return False

        return False

class IsAdministrator(BasePermission):
    def __init__(self):
        super().__init__()

    def has_permission(self, request, view):
        return self.validate_group('admin', request.auth)


