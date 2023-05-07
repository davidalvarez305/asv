#!/bin/sh

set -e

cd && cd /asv/website/

uwsgi --ini /etc/django.ini