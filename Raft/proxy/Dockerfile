# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo raft.proto desde la raíz del proyecto
COPY ../raft.proto ./

# Compilar el archivo proto para generar los archivos necesarios
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. raft.proto

# Copiar el resto de los archivos necesarios para el componente
COPY . .

# Instalar las dependencias necesarias
RUN pip install -r requirements.txt

# Comando para ejecutar el componente
CMD ["python", "proxy.py"]  # Cambia 'component.py' por el nombre correcto de tu archivo

