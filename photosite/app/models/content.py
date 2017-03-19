from __future__ import absolute_import

from django.db import models

from app.models.user import Company


class UploadItem(models.Model):
    url = models.URLField(max_length = 255, unique = True)
    processed = models.BooleanField(default = False)
    alerted = models.BooleanField(default = False)
    retrieved = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    company = models.ForeignKey(Company)

    class Meta:
        db_table = 'item'

    def __str__(self):
        return 'ID [{}] Uploaded [{}] Processed [{}] URL [{}]'.format(self.id, self.timestamp.strftime("%c"),
                                                                      self.processed, self.url)


class Image(models.Model):
    full_size = models.ImageField(upload_to = "images/fullsize", default = '')
    thumb = models.ImageField(upload_to = "images/thumbs", default = '')

    def generate_thumbnail(self):
        # TODO move to defined Celery task
        if not self.full_size:
            return

        import mimetypes
        import os
        from io import BytesIO
        from PIL import Image

        from django.core.files.uploadedfile import SimpleUploadedFile

        THUMBNAIL_SIZE = (100, 66) # max width, max height of thumbnail
        CONTENT_TYPE = mimetypes.guess_type(self.full_size.path)

        extension = 'jpeg'

        if CONTENT_TYPE[0] == 'image/jpeg':
            extension = 'jpeg',
        elif CONTENT_TYPE[0] == 'image/png':
            extension = 'png'


        image = Image.open(BytesIO(self.full_size.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        temp_handle = BytesIO()
        image.save(temp_handle, extension)
        temp_handle.seek(0)

        file_name = os.path.split('/', 1)[1]

        suf = SimpleUploadedFile(file_name, temp_handle.read(), CONTENT_TYPE[0])
        self.thumb.save(file_name, suf, save = False)


    class Meta:
        db_table = 'image'