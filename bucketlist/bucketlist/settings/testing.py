"""
Test specific settings.
"""
import os

if os.getenv('TRAVIS') is None:
    from django_envie.workroom import convertfiletovars
    convertfiletovars()

import logging
from .base import *

logging.disable(logging.CRITICAL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'test.db')
    }
}
