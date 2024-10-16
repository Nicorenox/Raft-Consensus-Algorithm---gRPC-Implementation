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
        put_response = stub.PutData(PutDataRequest(key='key1', data='value1'))
        logging.info("Respuesta de PutData: %s", put_response.success)

        # Ejemplo de lectura
        get_response = stub.GetData(GetDataRequest(key='key1'))
        logging.info("Respuesta de GetData: %s", get_response.value)

if __name__ == '__main__':
    main()
