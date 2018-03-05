from __future__ import absolute_import

import os
import requests
import mimetypes

from django.core.files import File
from rest_framework.test import APITestCase

from app.models import Company
from app.models import User
from photosite.settings.custom_storages import MediaStorage

from app.models.content import Image

class ImageTestCase(APITestCase):
    def setUp(self):
        self.path = os.path.join(os.path.expanduser('~'), 'project/action_me.jpg')
        self.username = "admin"
        self.email = "test@admin.com"
        self.password = "default123"
        self.admin = User.objects.create_superuser(username = self.username,
                                                   password = self.password,
                                                   email = self.email)

        self.company, created = Company.objects.get_or_create(name = 'test')

        self.admin.company = self.company
        self.admin.save()

    def test_s3_put(self):
        f = File(open(self.path, 'rb'), name = "action_me.jpg")
        test_image = Image.objects.create(full_size = f)
        test_image.save()

        file_type = mimetypes.guess_type(self.path)[0]

        self.assertEquals(file_type, 'image/jpeg')
        self.assertIsInstance(test_image.full_size.storage, MediaStorage)
        self.assertEquals(test_image.full_size.name, "images/action_me.jpg")
        test_image.full_size.delete()

    def test_s3_get(self):

        response = self.client.post('/upload', {
            'resource': 'https://s3.us-east-2.amazonaws.com/jasonjohns-photosite-ev/media/archives/test.zip',
            'password': 'default123',
            'event': 'basketball',
            'client': 'test'
        })

        self.assertEquals(201, response.status_code)
