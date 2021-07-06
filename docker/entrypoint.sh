#!/bin/sh

cat /app/docker/uwsgi.ini.template | sed -e "s/EMTSV_NUM_PROCESSES/${EMTSV_NUM_PROCESSES}/" > /app/docker/uwsgi.ini

if [ -z "$@" ]; then
    uwsgi --ini /app/docker/uwsgi.ini --die-on-term
else
    python3 /app/main.py "$@"
fi
