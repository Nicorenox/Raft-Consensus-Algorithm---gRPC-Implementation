import grpc
import logging
from raft_pb2 import PutDataRequest, GetDataRequest
from raft_pb2_grpc import RaftServiceStub

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    with grpc.insecure_channel('proxy:50050') as channel:
        stub = RaftServiceStub(channel)
        
        # Ejemplo de escritura
        key = "test_key"
        value = "test_value"
        response = stub.PutData(PutDataRequest(key=key, data=value))
        logging.info("Respuesta de escritura: %s", response.success)

        # Ejemplo de lectura
        response = stub.GetData(GetDataRequest(key=key))
        logging.info("Respuesta de lectura: %s", response.value)

if __name__ == '__main__':
    main()
