import os
from flask import Flask, request, jsonify, redirect
import pymysql

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "app_password")
DB_NAME = os.getenv("DB_NAME", "legacydb")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )

@app.get("/")
def home():
    return jsonify({
        "service": "TechNova API",
        "status": "running",
        "version": "2.0.0"
    }), 200

@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200

@app.get("/dashboard")
def dashboard_redirect():
    return redirect("/kuma/dashboard", code=302)

@app.get("/buscar")
def buscar_usuario():
    usuario_id = request.args.get("id", "1")

    try:
        usuario_id = int(usuario_id)
    except (TypeError, ValueError):
        return jsonify({"error": "El id debe ser un número entero"}), 400

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre FROM usuarios WHERE id = %s",
                (usuario_id,)
            )
            usuario = cursor.fetchone()
        conn.close()
        return jsonify({"usuario": usuario}), 200
    except pymysql.MySQLError as exc:
        app.logger.error("Error de base de datos: %s", exc)
        return jsonify({"error": "No fue posible consultar la base de datos"}), 503

if __name__ == "__main__":
    app.run(host=os.getenv("APP_HOST"), port=5050)
