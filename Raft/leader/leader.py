import grpc
import time
from concurrent import futures
from raft_pb2 import AppendEntriesRequest, AppendEntriesResponse
from raft_pb2_grpc import RaftServiceServicer, add_RaftServiceServicer_to_server

class RaftLeader(RaftServiceServicer):
    def __init__(self):
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.followers = ["follower1:50051", "follower2:50052"]

    def AppendEntries(self, request, context):
        if request.term < self.current_term:
            return AppendEntriesResponse(term=self.current_term, success=False)
        self.current_term = request.term
        # Logic for appending entries to the log
        return AppendEntriesResponse(term=self.current_term, success=True)

    def send_heartbeat(self):
        while True:
            time.sleep(1)  # Send heartbeat every second
            for follower in self.followers:
                with grpc.insecure_channel(follower) as channel:
                    stub = RaftServiceStub(channel)
                    try:
                        response = stub.AppendEntries(AppendEntriesRequest(term=self.current_term, leaderId="leader"))
                    except grpc.RpcError:
                        print(f"Follower {follower} is down.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RaftServiceServicer_to_server(RaftLeader(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("Leader server started.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

