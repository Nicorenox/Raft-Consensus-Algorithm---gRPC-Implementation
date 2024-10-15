# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto a la imagen
COPY raft.proto ./
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. raft.proto

# Instalar las dependencias necesarias
RUN pip install -r requirements.txt

# Comando para ejecutar el cliente
CMD ["python", "client.py"]