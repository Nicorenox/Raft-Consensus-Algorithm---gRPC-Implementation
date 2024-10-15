# Usar una imagen base de Python con soporte para gRPC
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto a la imagen
COPY raft.proto ./
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. raft.proto

# Instalar las dependencias necesarias
RUN pip install -r requirements.txt

# Exponer el puerto de la aplicación gRPC
EXPOSE 50050 50051 50052

# Comando para ejecutar el servidor 
CMD ["python", "follower.py"]
