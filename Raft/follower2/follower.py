import grpc
import time
from concurrent import futures
from raft_pb2 import AppendEntriesRequest, AppendEntriesResponse, VoteRequest, VoteResponse
from raft_pb2_grpc import RaftServiceServicer, add_RaftServiceServicer_to_server, RaftServiceStub

class RaftFollower(RaftServiceServicer):
    def __init__(self, follower_id):
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.follower_id = follower_id
        self.leader_timeout = 3  # Timeout for leader's heartbeat
        self.last_heartbeat = time.time()

    def AppendEntries(self, request, context):
        if request.term < self.current_term:
            return AppendEntriesResponse(term=self.current_term, success=False)
        self.current_term = request.term
        self.last_heartbeat = time.time()  # Reset heartbeat timer
        # Append entries logic
        return AppendEntriesResponse(term=self.current_term, success=True)

    def check_leader_timeout(self):
        if time.time() - self.last_heartbeat > self.leader_timeout:
            self.start_election()

    def start_election(self):
        self.current_term += 1
        print(f"Follower {self.follower_id} starting election for term {self.current_term}")
        self.voted_for = self.follower_id
        vote_count = 1  # Vote for self
        followers = ["follower1:50051", "follower2:50052"]

        for follower in followers:
            with grpc.insecure_channel(follower) as channel:
                stub = RaftServiceStub(channel)
                try:
                    response = stub.RequestVote(VoteRequest(term=self.current_term, candidateId=self.follower_id))
                    if response.voteGranted:
                        vote_count += 1
                except grpc.RpcError:
                    print(f"Follower {follower} is down.")

        if vote_count > len(followers) // 2:
            print(f"Follower {self.follower_id} becomes the new leader!")

def serve(follower_id, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RaftServiceServicer_to_server(RaftFollower(follower_id), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Follower {follower_id} server started on port {port}.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve("follower1", 50051)

