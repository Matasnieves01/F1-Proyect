# Dockerfile
FROM python:3.11-slim
# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc postgresql libpq-dev \
    pkg-config && \
    apt-get clean


# Crear directorio
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt


# Copiar el resto del proyecto
COPY . /app

# Comando por defecto
CMD [""]
