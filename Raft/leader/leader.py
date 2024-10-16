import grpc
import logging
import time
from concurrent import futures
from raft_pb2 import AppendEntriesRequest, AppendEntriesResponse, PutDataRequest, GetDataRequest, GetDataResponse
from raft_pb2_grpc import RaftServiceServicer, add_RaftServiceServicer_to_server

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RaftLeader(RaftServiceServicer):
    def __init__(self):
        self.current_term = 0
        self.voted_for = None
        self.log = {}
        self.commit_index = 0
        self.last_applied = 0
        self.followers = ["follower1:50051", "follower2:50052"]
        logging.info("Líder inicializado con seguidores: %s", self.followers)

    def PutData(self, request, context):
        logging.info("Recibiendo solicitud de escritura: %s", request.data)
        self.log[request.key] = request.data
        return GetDataResponse(success=True)

    def GetData(self, request, context):
        logging.info("Recibiendo solicitud de lectura para la clave: %s", request.key)
        value = self.log.get(request.key, "No existe")
        return GetDataResponse(value=value)

    def AppendEntries(self, request, context):
        if request.term < self.current_term:
            logging.warning("Término de solicitud de AppendEntries es menor al término actual.")
            return AppendEntriesResponse(term=self.current_term, success=False)
        self.current_term = request.term
        logging.info("Término actualizado a %d", self.current_term)
        return AppendEntriesResponse(term=self.current_term, success=True)

    def send_heartbeat(self):
        while True:
            time.sleep(1)  # Heartbeat cada segundo
            for follower in self.followers:
                with grpc.insecure_channel(follower) as channel:
                    stub = RaftServiceStub(channel)
                    try:
                        logging.info("Enviando heartbeat al seguidor %s", follower)
                        response = stub.AppendEntries(AppendEntriesRequest(term=self.current_term, leaderId="leader"))
                    except grpc.RpcError:
                        logging.error("Seguidor %s caído.", follower)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RaftServiceServicer_to_server(RaftLeader(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    logging.info("Servidor líder iniciado en el puerto 50050")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
