import os
import requests
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de nodos del servidor
nodes = ["http://node1:5000", "http://node2:5000", "http://node3:5000"]

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/write", methods=["POST"])
def write():
    data = request.get_json()
    logging.info(f"Recibida solicitud de escritura: {data}")

    # Redirigir a un nodo líder para escribir
    for node in nodes:
        try:
            response = requests.post(f"{node}/write", json=data, timeout=1)
            if response.status_code == 200:
                logging.info(f"Escritura exitosa en {node}: {response.json()}")
                return jsonify({"status": "success", "message": response.json()["message"]})
        except requests.exceptions.RequestException as e:
            logging.warning(f"Fallo al contactar {node}: {str(e)}")
            continue

    logging.error("No se encontró un líder disponible para la operación de escritura.")
    return jsonify({"error": "No leader available"}), 503

@app.route("/read", methods=["GET"])
def read():
    logging.info("Recibida solicitud de lectura.")

    # Redirigir a un nodo follower para leer
    for node in nodes:
        try:
            response = requests.get(f"{node}/read", timeout=1)
            if response.status_code == 200:
                logging.info(f"Lectura exitosa de {node}: {response.json()}")
                return jsonify({"status": "success", "data": response.json()["data"]})
        except requests.exceptions.RequestException as e:
            logging.warning(f"Fallo al contactar {node}: {str(e)}")
            continue

    logging.error("No se encontró un follower disponible para la operación de lectura.")
    return jsonify({"error": "No follower available"}), 503

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)
