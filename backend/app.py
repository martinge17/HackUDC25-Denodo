from flask import Flask, request, jsonify
import requests
import sqlite3
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# URL del Servicio Denodo
DENODO_URL = os.environ.get("DENODO_URL")

# Credenciales para autenticación básica en Denodo
DENODO_AUTH = (os.environ.get("USER"), os.environ.get("PASS"))

# Ruta de la base de datos SQLite
DATABASE = "data/history.db"


# Crear tabla si no existe
def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                chat_id TEXT NOT NULL,
                msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


init_db()  # Inicializar la base de datos al iniciar el servicio


@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    chat_id = data.get("chat_id", "")
    user_message = data.get("message", "")

    if not chat_id or not user_message:
        return jsonify({"error": "chat_id y message son obligatorios"}), 400

    try:
        # Parámetros de la consulta a Denodo
        params = {
            "question": user_message,
            "plot": False,
            "embeddings_provider": "googleaistudio",
            "embeddings_model": "models/text-embedding-004",
            "vector_store_provider": "Chroma",
            "sql_gen_provider": "googleaistudio",
            "sql_gen_model": "gemini-1.5-flash",
            "chat_provider": "googleaistudio",
            "chat_model": "gemini-1.5-flash",
            "vdp_database_names": "samples_bank",
            "custom_instructions": "Eres un experto en los juegos olimpicos de 2024 y tambien en realizar consultas sql muy precisas",
            "expand_set_views": True,
            "markdown_response": True,
            "vector_search_k": 5,
            "mode": "default",
            "disclaimer": True,
            "verbose": True,
        }

        # Enviar la consulta a Denodo
        response = requests.get(
            DENODO_URL,
            params=params,
            auth=DENODO_AUTH,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()

        # Procesar la respuesta
        denodo_response = response.json()
        respuesta = denodo_response.get("answer", "")

        # Guardar pregunta y respuesta en la base de datos
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (chat_id, pregunta, respuesta) VALUES (?, ?, ?)",
                (chat_id, user_message, respuesta),
            )
            conn.commit()

        return jsonify(
            {"chat_id": chat_id, "pregunta": user_message, "respuesta": respuesta}
        )

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history/<chat_id>", methods=["GET"])
def get_chat_history(chat_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT msg_id, pregunta, respuesta, timestamp FROM chat_history WHERE chat_id = ? ORDER BY msg_id ASC",
                (chat_id,),
            )
            rows = cursor.fetchall()

        history = [
            {
                "msg_id": row[0],
                "pregunta": row[1],
                "respuesta": row[2],
                "timestamp": row[3],
            }
            for row in rows
        ]

        return jsonify({"chat_id": chat_id, "mensajes": history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chats", methods=["GET"])
def get_chat_ids():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT chat_id FROM chat_history ORDER BY chat_id ASC"
            )
            rows = cursor.fetchall()

        chat_ids = [row[0] for row in rows]  # Extrae solo los chat_id

        return jsonify({"chats": chat_ids})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
