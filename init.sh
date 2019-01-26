#!/bin/bash

./wait-for-it.sh db:5432 -t 300
sleep 10

echo "Postgres is up"

python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
python manage.py runserver 0.0.0.0:8000
