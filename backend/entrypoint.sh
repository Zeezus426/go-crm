#!/bin/sh
chmod +x manage.py
python manage.py migrate
daphne -b 0.0.0.0 -p 8000  --proxy-headers core.asgi:application