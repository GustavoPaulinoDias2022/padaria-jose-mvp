#!/usr/bin/env bash
set -euo pipefail
# Um serviço/instância de demonstração. Para múltiplas instâncias, separar migrações em release job.
python manage.py migrate --noinput
python manage.py bootstrap_owner
python manage.py seed_demo
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-10000}" --workers 1 --threads 2 --timeout 60
