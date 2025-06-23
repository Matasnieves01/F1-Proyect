# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc postgresql libpq-dev \
    pkg-config && \
    apt-get clean


# Crear directorio
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install -r /app/requirements.txt


# Copiar el resto del proyecto
COPY .. .

# Comando por defecto
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 config.asgi:application"]
