import grpc
import logging
import time
from concurrent import futures
from raft_pb2 import AppendEntriesRequest, GetDataResponse, PutDataRequest, GetDataRequest
from raft_pb2_grpc import RaftServiceServicer, add_RaftServiceServicer_to_server, RaftServiceStub

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RaftFollower(RaftServiceServicer):
    def __init__(self, follower_id):
        self.current_term = 0
        self.voted_for = None
        self.log = {}
        self.commit_index = 0
        self.last_applied = 0
        self.follower_id = follower_id
        self.leader_timeout = 3  # Timeout para heartbeat
        self.last_heartbeat = time.time()
        logging.info("Seguidor %s inicializado", follower_id)

    def PutData(self, request, context):
        logging.warning("Solicitud de escritura recibida en el seguidor, no se permite.")
        return GetDataResponse(success=False)

    def GetData(self, request, context):
        logging.info("Recibiendo solicitud de lectura para la clave: %s", request.key)
        value = self.log.get(request.key, "No existe")
        return GetDataResponse(value=value)

    def AppendEntries(self, request, context):
        if request.term < self.current_term:
            logging.warning("Término de AppendEntries es menor al término actual en el seguidor.")
            return AppendEntriesResponse(term=self.current_term, success=False)
        self.current_term = request.term
        self.last_heartbeat = time.time()  # Resetear el temporizador de heartbeat
        logging.info("Heartbeat recibido, término actualizado a %d", self.current_term)
        return AppendEntriesResponse(term=self.current_term, success=True)

    def check_leader_timeout(self):
        if time.time() - self.last_heartbeat > self.leader_timeout:
            logging.warning("Timeout del líder, iniciando elección.")
            self.start_election()

    def start_election(self):
        self.current_term += 1
        logging.info("Iniciando elección para el término %d", self.current_term)
        self.voted_for = self.follower_id
        vote_count = 1  # Voto por sí mismo
        followers = ["follower1:50051", "follower2:50052"]

        for follower in followers:
            with grpc.insecure_channel(follower) as channel:
                stub = RaftServiceStub(channel)
                try:
                    response = stub.RequestVote(VoteRequest(term=self.current_term, candidateId=self.follower_id))
                    if response.voteGranted:
                        vote_count += 1
                        logging.info("Voto recibido del seguidor %s", follower)
                except grpc.RpcError:
                    logging.error("El seguidor %s está caído.", follower)

        if vote_count > len(followers) // 2:
            logging.info("El seguidor %s se convierte en el nuevo líder.", self.follower_id)

def serve(follower_id, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RaftServiceServicer_to_server(RaftFollower(follower_id), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info("Servidor seguidor %s iniciado en el puerto %s.", follower_id, port)
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve("follower1", 50051)
