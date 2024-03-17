FROM piklema_backend_base

WORKDIR /app

COPY . /app

CMD sh -c "python manage.py migrate && gunicorn config.wsgi --log-level debug --access-logfile ./logs/gunicorn_access.log --error-logfile ./logs/gunicorn_error.log --bind 0.0.0.0:8000 --workers 1"
# CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
