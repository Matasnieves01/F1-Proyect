# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc postgresql libpq-dev \
    default-libmysqlclient-dev pkg-config && \
    apt-get clean


# Crear directorio
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY .. .

# Comando por defecto
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
