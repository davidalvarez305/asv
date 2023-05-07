#!/bin/sh

set -e

cd && cd ./website/

uwsgi --ini /etc/django.ini