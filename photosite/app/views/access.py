from __future__ import absolute_import

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.permissions import IsAdministrator, IsValidToken
from app.models.user import User
from app.serializers.user import UserSerializer
from app.views import AbstractView


@permission_classes((IsValidToken, ))
class LogoutView(AbstractView):
    def __init__(self):
        super().__init__()

    def post(self, request):
        try:
            user = User.objects.get(token = request.auth)
            user.token = ''
            user.save()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist as e:
            self.log.error('User id does not exist for token [{]'.format(request.auth))
            return self.error_response('User with token does not exist')



@permission_classes((IsAdministrator, ))
class RegistrationView(AbstractView):
    def __init__(self):
        super().__init__()




@permission_classes((AllowAny, ))
class LoginView(AbstractView):
    def __init__(self):
        super().__init__()

    def _authenticate(self, username, password):
        if username and password:
            try:
                user = User.objects.get(username = username)
                if user and user.check_password(password):
                    return user, ''

                return None, 'Password invalid for this user'
            except User.DoesNotExist as e:
                self.log.error('User with username [{}] does not exist'.format(username))
                return None, 'Username does not exist'

        return None, 'Invalid Credentials'

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user, message = self._authenticate(username, password)

        if user is None:
            return self.error_response(message, status.HTTP_401_UNAUTHORIZED)

        if user.is_active:
            user.generate_token()
            serializer = UserSerializer(user)
            return Response(serializer)

        else:
            return self.error_response('Account disabled', status.HTTP_401_UNAUTHORIZED)

