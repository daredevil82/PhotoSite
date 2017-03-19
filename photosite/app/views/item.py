from __future__ import absolute_import

import os
import requests


from io import BytesIO
from zipfile import ZipFile

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from photosite.settings import EXTRACT_PATH

from app.models.user import Company, User
from app.models.content import Image, UploadItem
from app.views import AbstractView

class UploadItemView(AbstractView):
    def __init__(self):
        super().__init__()

    def extract_images(self, archive_url):
        self.log.info('Retrieving and extracting images from [{}]'.format(archive_url))
        try:
            req = requests.get(archive_url, stream = True)
            if req.status_code < 400:
                zip = ZipFile(BytesIO(req.content))
                item_count = 0

                if not os.path.exists(EXTRACT_PATH):
                    os.makedirs(EXTRACT_PATH)

                for item in zip.namelist():
                    if item.startswith('edits'):
                        item_count+= 1
                        zip.extract(item, EXTRACT_PATH)

                req.close()
                self.log.info('[{}] items extracted to [{}]'.format(item_count, EXTRACT_PATH))
                return True

            else:
                req.close()
                raise requests.RequestException('Request status code: [{}]'.format(req.status_code))
        except requests.RequestException as e:
            self.log.error('Error retrieving URL [{}].  Message: [{}]'.format(archive_url, e))
            raise requests.RequestException(e)

    def is_admin(self, password):
        try:
            admin = User.objects.get(username = 'admin')
            if admin.check_password(password):
                return True
            else:
                return False

        except User.DoesNotExist:
            self.log.error('Administrator account \'admin\' does not exist')
            return False



    def post(self, request):
        data = request.data

        if 'resource' in data and 'password' in data and 'client' in data:
            self.log.info('Valid UploadItem request received')

            if self.is_admin(data['password']):
                try:
                    client = Company.objects.get(name = data['client'])
                    item, created = UploadItem.objects.get_or_create(url = data['resource'], company = client)

                    item.company = client
                    item.save()
                    self.extract_images(data['resource'])
                    return Response(status= status.HTTP_201_CREATED)


                except Company.DoesNotExist as e:
                    self.log.error('Client [{}] does not exist'.format(data['client']))
                    return self.error_response('Client [{}] does not exist'.format(data['client']))
                except requests.RequestException as e:
                    self.log.error(e)
                    return self.error_response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

            return self.error_response('Check password failed', status.HTTP_403_FORBIDDEN)

        else:
            self.log.error('Invalid UploadItem request received. [{}]'.format(data))
            return self.error_response('Invalid UploadItem request', status.HTTP_400_BAD_REQUEST)