#!/bin/sh

set -e

cd && cd /asv/website/

python manage.py collectstatic --noinput

uwsgi --ini /etc/django.ini