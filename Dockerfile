
FROM python:3.13-slim

# Evitar archivos temporales de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario sin privilegios
RUN addgroup --system django && adduser --system --ingroup django django

# Copiar proyecto
COPY . .

# Preparar permisos de almacenamiento
RUN mkdir -p /app/data && chown -R django:django /app

# Ejecutar con usuario sin privilegios
USER django

# Puerto de Django
EXPOSE 8000

# Ejecutar migraciones e iniciar Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
