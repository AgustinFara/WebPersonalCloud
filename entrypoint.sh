#!/bin/bash
set -e

# Inyectamos la IP en el archivo hosts en tiempo de ejecución
echo "35.214.212.185 db.fpbftsgvsyiidcgbfvgw.supabase.co" >> /etc/hosts

# Intentar forzar IPv4 usando un comando de ping rápido para "calentar" el DNS
# o simplemente esperar a que el puerto 5432 esté abierto
echo "Esperando a que la base de datos esté lista..."

while ! nc -z -w 5 db.fpbftsgvsyiidcgbfvgw.supabase.co 5432; do
  echo "La base de datos aún no responde, esperando..."
  sleep 2
done

echo "Base de datos conectada. Ejecutando migraciones..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn webpersonal.wsgi:application --bind 0.0.0.0:8080