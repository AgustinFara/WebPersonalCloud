# 1. Imagen base
FROM python:3.11-slim


# Instalar dependencias del sistema necesarias para Pillow
RUN apt-get update && apt-get install -y netcat-traditional \
    build-essential \
    zlib1g-dev \
    libjpeg-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Configuración de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 4. Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el código
COPY . .

# COMPILACIÓN DE IDIOMAS
# Compila apuntando solo a los idiomas del proyecto (en, it)
 RUN python manage.py compilemessages -l en -l it


EXPOSE 8080

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]