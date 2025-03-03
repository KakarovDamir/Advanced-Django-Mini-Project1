#!/bin/bash

# Wait for postgres
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

case "$1" in
    "web")
        # Create migrations directory if it doesn't exist
        mkdir -p users/migrations
        touch users/migrations/__init__.py
        
        # Remove existing migrations and pyc files
        find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
        find . -path "*/migrations/*.pyc" -delete
        
        # Make fresh migrations for all apps
        python manage.py makemigrations
        
        # Apply migrations in the correct order
        python manage.py migrate --fake-initial
        python manage.py migrate auth
        python manage.py migrate admin
        python manage.py migrate contenttypes
        python manage.py migrate sessions
        python manage.py migrate users
        python manage.py migrate trading
        python manage.py migrate analytics
        python manage.py migrate products
        python manage.py migrate sales
        python manage.py migrate notifications
        
        # Create superuser if it doesn't exist
        DJANGO_SUPERUSER_USERNAME=admin \
        DJANGO_SUPERUSER_EMAIL=admin@example.com \
        DJANGO_SUPERUSER_PASSWORD=admin \
        python manage.py createsuperuser --noinput || true
        
        # Start server
        python manage.py runserver 0.0.0.0:8000
        ;;
    "celery")
        celery -A sales_trading_app worker --loglevel=info
        ;;
    "celery-beat")
        celery -A sales_trading_app beat --loglevel=info
        ;;
    *)
        exec "$@"
        ;;
esac 