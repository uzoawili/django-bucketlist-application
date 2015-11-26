"""
Settings package initialization.
"""

import os

if os.getenv('DEPLOY') == 'PRODUCTION':
	from production import *
else:
	# load and set environment variables from '.env.yml' or '.env.py' files with django_envie
    from django_envie.workroom import convertfiletovars
    convertfiletovars()

    from development import *
