# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY server.py /app/server.py
COPY requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto 5000
EXPOSE 5000

# Comando para iniciar el servidor
CMD ["python", "server.py"]
