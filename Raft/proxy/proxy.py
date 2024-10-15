import grpc
from concurrent import futures
import raft_pb2
import raft_pb2_grpc

# Aquí se define la clase del proxy que manejará las solicitudes del cliente
class RaftProxyServicer(raft_pb2_grpc.RaftServiceServicer):
    
    def __init__(self, leader_ip, follower_ips):
        self.leader_ip = leader_ip
        self.follower_ips = follower_ips
    
    def GetData(self, request, context):
        # Redirige la solicitud de lectura a uno de los followers
        follower_channel = grpc.insecure_channel(self.follower_ips[0] + ':50051')  # Asume follower1
        follower_stub = raft_pb2_grpc.RaftServiceStub(follower_channel)
        return follower_stub.GetData(request)
    
    def PutData(self, request, context):
        # Redirige la solicitud de escritura al líder
        leader_channel = grpc.insecure_channel(self.leader_ip + ':50050')
        leader_stub = raft_pb2_grpc.RaftServiceStub(leader_channel)
        return leader_stub.PutData(request)

# Configura y ejecuta el servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftProxyServicer('leader_ip', ['follower1_ip', 'follower2_ip']), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("Proxy server running on port 50050")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
