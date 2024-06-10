#!/bin/bash
exec gunicorn proyectois.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3