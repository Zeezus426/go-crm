#!/bin/sh
chmod +x manage.py
python manage.py migrate
daphne -b 0.0.0.0 -p 80  --proxy-headers djecommerce.asgi:application