# Usa la imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo proto
COPY raft.proto ./

# Copiar los archivos del proyecto a la imagen
COPY . .

# Instala las dependencias necesarias
RUN pip install grpcio grpcio-tools

# Compila el archivo proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. raft.proto

# Exponer el puerto de la aplicación gRPC
EXPOSE 50050 50051 50052 50053

# Comando para ejecutar el servidor 
CMD ["python", "leader.py"]
