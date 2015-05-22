web: gunicorn -b 0.0.0.0:$PORT --log-file - wsgi
celeryd: python manage.py celeryd -E -l info -c 2