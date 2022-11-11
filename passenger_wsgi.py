# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1813889/data/www/wolf-mag.ru/tga')
sys.path.insert(1, '/var/www/u1813889/data/djangoenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tga.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()