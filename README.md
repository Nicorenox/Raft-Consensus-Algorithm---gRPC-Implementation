# Raft Project

This project implements a consensus system using the Raft algorithm in Python. The system consists of three nodes that simulate a working environment in a cluster, and a proxy that handles read and write operations. The architecture is designed to provide high availability and reliability through leadership and node voting.

## Introduction to Raft

Raft is a consensus algorithm that is much simpler to understand compared to Paxos, but it achieves the same goals: maintaining consistency in a distributed system even when some nodes fail. Raft uses a strong leader and is divided into three main components:

1. **Leader Election**: A new leader is elected when the current leader fails or becomes unreachable.
2. **Log Replication**: The leader receives commands from clients and replicates the log entries across all follower nodes.
3. **Safety**: Raft ensures that logs are applied in the same order across all nodes, guaranteeing consistency.

The Raft algorithm operates in terms of **terms**, where each term begins with an election. If a leader is successfully elected, it serves during that term; otherwise, a new term begins.
For a more visual explanation of the Raft algorithm, please visit [this page](https://thesecretlivesofdata.com/raft/).

## Component Descriptions

- **server.py**: Implements the logic of the Raft algorithm, manages read and write operations, and handles leadership among nodes.
- **client.py**: Allows the user to perform read and write operations through the proxy.
- **proxy.py**: Acts as an intermediary between the client and nodes, redirecting requests as needed.
- **Dockerfile**: Defines the configuration for the server image.
- **Dockerfile.client**: Defines the configuration for the client image.
- **Dockerfile.proxy**: Defines the configuration for the proxy image.
- **docker-compose.yml**: Defines and runs the containers for the nodes and the proxy

## How the System Works

### Leader Election

Leader election happens when:

1. A follower does not receive a heartbeat from the leader for a predefined election timeout.
2. The follower becomes a candidate and starts an election by requesting votes from other nodes.
3. Each node votes only once per term and votes for the first candidate it hears from.
4. If a candidate receives a majority of votes, it becomes the leader.
5. The new leader sends heartbeats to other followers to establish its authority.

If the election results in a tie, the term ends without a leader, and a new election is triggered with a higher term number.

### Heartbeats

The leader sends **heartbeats** to followers regularly to prevent them from starting an election. Heartbeats are a special case of the `AppendEntries` RPC, which includes no log entries but only a signal from the leader to maintain leadership status. This keeps the cluster stable as long as the leader is functioning properly.

- Heartbeats are sent periodically (e.g., every second).
- If a follower does not receive a heartbeat within the election timeout, it assumes the leader is down and starts a new election.

### Log Replication

The leader is responsible for accepting client commands, adding them to its own log, and replicating the logs across all followers. The followers then confirm they have stored the entries, and the leader applies the entries to its state machine once they are committed.

1. **Client sends command**: The leader receives a command from a client.
2. **Append entries**: The leader appends the command to its own log.
3. **Replicate logs**: The leader sends the new log entry to all followers using `AppendEntries` RPCs.
4. **Commit logs**: Once the majority of followers have stored the entry, the leader marks the entry as committed and applies it to its state machine.
5. **Apply logs**: Followers apply committed logs in the same order as the leader.

### Log Consistency

Raft ensures consistency by maintaining the following invariants:

1. If two logs on different servers are identical up to a certain point, then any subsequent logs must also be identical.
2. If a follower is missing log entries, the leader will overwrite the follower's log to ensure that all nodes have the same log.
3. A log entry is considered committed once the leader has replicated it to a majority of nodes.

### Handling Failures

Raft is designed to handle failures efficiently, ensuring that the system remains operational even when some nodes go down:

1. **Leader Failure**: If the leader fails, an election is triggered by followers, and a new leader is elected.
2. **Follower Failure**: If a follower fails, the leader continues to operate. When the follower comes back online, it receives any missing log entries from the leader to catch up.
3. **Network Partitions**: Raft can handle network partitions, ensuring that nodes in the majority partition elect a new leader and continue to function, while nodes in the minority partition fall back to a follower state.

## Logging and Debugging

The system uses Python's built-in `logging` module to provide detailed logs for all the key operations:

- **Leader**: Logs heartbeats sent to followers, log replication progress, and term updates.
- **Follower**: Logs received heartbeats, votes cast during elections, and log entries received.
- **Candidate**: Logs vote requests and election outcomes.
- **Errors**: Any network failures or RPC errors are logged to help with debugging.

You can adjust the verbosity of the logs by changing the logging level in the code (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## Author

- Developed by [Nicolas Moreno Lopez](https://github.com/Nicorenox)
