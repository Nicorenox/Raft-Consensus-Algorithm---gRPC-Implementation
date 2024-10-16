import grpc
import logging
from concurrent import futures
from raft_pb2 import GetDataRequest, PutDataRequest
from raft_pb2_grpc import RaftServiceServicer, add_RaftServiceServicer_to_server, RaftServiceStub

# Configurar el logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class RaftProxyServicer(RaftServiceServicer):
    def __init__(self, leader_ip):
        self.leader_ip = leader_ip
        logging.info("Proxy inicializado con líder: %s", leader_ip)

    def GetData(self, request, context):
        logging.info("Solicitud de lectura recibida, redirigiendo al líder.")
        with grpc.insecure_channel(self.leader_ip) as channel:
            stub = RaftServiceStub(channel)
            return stub.GetData(request)

    def PutData(self, request, context):
        logging.info("Solicitud de escritura recibida, redirigiendo al líder.")
        with grpc.insecure_channel(self.leader_ip) as channel:
            stub = RaftServiceStub(channel)
            return stub.PutData(request)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RaftServiceServicer_to_server(RaftProxyServicer('leader:50050'), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    logging.info("Servidor proxy iniciado en el puerto 50050")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
