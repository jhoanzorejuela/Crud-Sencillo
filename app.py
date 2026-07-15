from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)
DB_FILE = "estudiantes.json"

def cargar_datos():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/estudiantes", methods=["GET"])
def obtener_estudiantes():
    return jsonify(cargar_datos())

@app.route("/api/estudiantes", methods=["POST"])
def crear_estudiante():
    datos = cargar_datos()
    nuevo = request.json
    nuevo["id"] = max([e["id"] for e in datos], default=0) + 1
    datos.append(nuevo)
    guardar_datos(datos)
    return jsonify(nuevo), 201

@app.route("/api/estudiantes/<int:id>", methods=["PUT"])
def actualizar_estudiante(id):
    datos = cargar_datos()
    for i, e in enumerate(datos):
        if e["id"] == id:
            datos[i] = {**request.json, "id": id}
            guardar_datos(datos)
            return jsonify(datos[i])
    return jsonify({"error": "No encontrado"}), 404

@app.route("/api/estudiantes/<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    datos = cargar_datos()
    datos = [e for e in datos if e["id"] != id]
    guardar_datos(datos)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
