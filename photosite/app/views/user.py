from __future__ import absolute_import

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.permissions import IsAdministrator, IsValidToken
from app.models.user import User
from app.serializers.user import UserSerializer
from app.views import AbstractView


@permission_classes((IsAdministrator, ))
class UserListView(AbstractView):
    def __init__(self):
        super().__init__()

    def get(self, request):
        users = User.objects.all()
        serialized = UserSerializer(users, many = True)
        return Response(serialized.data)


@permission_classes((IsAdministrator, IsValidToken))
class UserDetailView(AbstractView):
    def __init__(self):
        super().__init__()

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk = user_id)
            serialized = UserSerializer(user)
            return Response(serialized.data)

        except User.DoesNotExist:
            return self.error_response('User [{}] does not exist'.format(user_id))
