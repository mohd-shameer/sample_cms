#!/bin/bash

while true; do
    postgres_res=`pg_isready -h postgres -p 5432`
    if [[ "$postgres_res" == *"accepting"* ]]; then
        break
    fi
    echo "Waiting for postgres connection..."
    sleep 3
done

echo "Postgres is running."

pg_user=`PGPASSWORD="$POSTGRES_PASSWORD" psql -h $POSTGRES_HOST -p 5432 -U $POSTGRES_USER -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_SUSER'"`
if [[ ! "$pg_user" ]]; then
    echo "Running the setup script"
    bash /root/setup.sh
fi

python3 /cms/manage.py makemigrations
python3 /cms/manage.py migrate

echo "Done."
python3 /cms/manage.py runserver 0.0.0.0:8000
