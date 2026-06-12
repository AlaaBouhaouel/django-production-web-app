web: python manage.py migrate && python manage.py createsuperuser --no-input || true && gunicorn atast.wsgi:application --bind 0.0.0.0:$PORT
