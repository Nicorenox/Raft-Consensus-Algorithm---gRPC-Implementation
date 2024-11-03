import os
import time
import random
import threading
import requests
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configuración básica de Raft
node_id = int(os.getenv("NODE_ID", 1))
nodes = ["http://node1:5000", "http://node2:5000", "http://node3:5000"]
leader = None
is_leader = False
term = 0
vote_count = 0

# Configuración de logging para Docker
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - Node {} - %(message)s'.format(node_id))

# Función para iniciar votación si el líder está inactivo
def start_election():
    global term, vote_count, leader, is_leader
    term += 1
    vote_count = 1  # Votamos por nosotros mismos
    is_leader = False
    leader = None
    logging.info(f"Starting election for term {term}")
    for node in nodes:
        if node != nodes[node_id - 1]:  # No votamos por nosotros mismos
            try:
                response = requests.post(f"{node}/vote", json={"term": term, "candidate_id": node_id}, timeout=1)
                if response.json().get("vote_granted"):
                    vote_count += 1
                    logging.info(f"Received vote from {node}")
            except requests.exceptions.RequestException:
                logging.warning(f"Node {node} did not respond to vote request.")
    if vote_count > len(nodes) // 2:  # Mayoría alcanzada
        leader = nodes[node_id - 1]
        is_leader = True
        logging.info("This node is now the leader")

# Endpoint para votar por un candidato
@app.route("/vote", methods=["POST"])
def vote():
    global term, leader
    data = request.get_json()
    candidate_term = data["term"]
    candidate_id = data["candidate_id"]
    if candidate_term > term:
        term = candidate_term
        leader = nodes[candidate_id - 1]
        logging.info(f"Voted for node {candidate_id} in term {term}")
        return jsonify({"vote_granted": True})
    return jsonify({"vote_granted": False})

# Endpoint para realizar heartbeat desde el líder
@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    global leader
    data = request.get_json()
    if "leader_id" in data:
        leader = nodes[data["leader_id"] - 1]
        logging.info(f"Received heartbeat from leader {data['leader_id']}")
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

# Operación de lectura (solo followers)
@app.route("/read", methods=["GET"])
def read():
    if is_leader:
        return jsonify({"error": "Leader cannot perform read operations"}), 403
    logging.info("Read request served")
    return jsonify({"status": "success", "data": "This is the data"})

# Operación de escritura (solo el líder)
@app.route("/write", methods=["POST"])
def write():
    if not is_leader:
        return jsonify({"error": "Only leader can perform write operations"}), 403
    data = request.get_json()
    logging.info(f"Write request with data: {data}")
    return jsonify({"status": "success", "message": "Data written successfully"})

# Función para manejar los heartbeats si el nodo es líder
def send_heartbeats():
    while True:
        if is_leader:
            for node in nodes:
                if node != nodes[node_id - 1]:  # No enviamos heartbeats a nosotros mismos
                    try:
                        requests.post(f"{node}/heartbeat", json={"leader_id": node_id}, timeout=1)
                    except requests.exceptions.RequestException:
                        logging.warning(f"Node {node} did not respond to heartbeat.")
        time.sleep(2)

# Función de verificación de líder para reiniciar elección si el líder falla
def check_leader():
    global leader
    while True:
        if leader and leader != nodes[node_id - 1]:
            try:
                response = requests.post(f"{leader}/heartbeat", json={"leader_id": node_id}, timeout=1)
                if response.status_code != 200:
                    logging.warning(f"Leader {leader} heartbeat failed.")
                    leader = None
                    start_election()
            except requests.exceptions.RequestException:
                logging.warning(f"Leader {leader} heartbeat failed.")
                leader = None
                start_election()
        elif leader is None:
            start_election()
        time.sleep(5)

# Inicio de los threads
if __name__ == "__main__":
    threading.Thread(target=send_heartbeats, daemon=True).start()
    threading.Thread(target=check_leader, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
