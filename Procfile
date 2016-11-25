web: gunicorn -w 2 -b :$PORT -e DEBUG=0 --log-file - server.wsgi:application
webdevel: DEBUG=1 python manage.py runserver 0.0.0.0:$PORT
