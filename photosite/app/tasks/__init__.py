from __future__ import absolute_import

import logging

from photosite.celery_config import app

class BaseTask(app.Task):

    def __init__(self):
        self.logger = logging.getLogger('django')



