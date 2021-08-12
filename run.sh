#!/bin/sh

python manage.py qcluster &
daphne -b 0.0.0.0 Mate365BillingPortal.asgi:application