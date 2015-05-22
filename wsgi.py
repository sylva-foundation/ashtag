import os
import sys
from path import path

sys.path.append(path(__file__).dirname() / 'src')
sys.path.append(path(__file__).dirname() / 'lib')

if 'CRED_FILE' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ashtag.settings.live')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ashtag.settings.localdev')

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())

