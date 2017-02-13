from __future__ import absolute_import

import os

from photosite.settings.local import LOG_FILE, LOG_LEVEL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': 'False',
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'level': LOG_LEVEL,
            'filename': os.path.join(LOG_FILE, 'django.log'),
        },
        'celery': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'level': LOG_LEVEL,
            'filename': os.path.join(LOG_FILE, 'celery.log')
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': LOG_LEVEL,
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'celery': {
            'handlers': ['file'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}