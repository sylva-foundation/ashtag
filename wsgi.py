import os
import sys
from path import path

sys.path.append(path(__file__).dirname() / 'src')
sys.path.append(path(__file__).dirname() / 'lib')

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())

