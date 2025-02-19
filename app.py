import json
import os
import unicodedata
from flask import Flask, request, jsonify

db_file = "usuarios.json"
app = Flask(__name__)

def guardar_datos(archivo, datos):
    """Guarda un diccionario en un archivo JSON con codificación UTF-8"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)  # Asegura que no guarde caracteres en formato \uXXXX

def cargar_datos(archivo):
    """Carga un diccionario desde un archivo JSON si existe con UTF-8"""
    if not os.path.exists(archivo):
        return {}
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalizar_texto(texto):
    """Elimina tildes, pasa a minúsculas y normaliza el texto"""
    if not texto:
        return ""
    texto = texto.strip()  # Elimina espacios innecesarios
    texto = texto.lower()  # Convierte a minúsculas
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')  # Quita tildes
    return texto

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    """Agrega un usuario a la base de datos con normalización"""
    datos = cargar_datos(db_file)
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    nombre_normalizado = normalizar_texto(nombre)

    if nombre_normalizado in datos:
        return jsonify({"error": "Usuario ya existe"}), 400

    datos[nombre_normalizado] = {
        "nombre_original": nombre,  # Guardamos el nombre original con tildes
        "edad": data.get("edad"),
        "email": data.get("email")
    }
    guardar_datos(db_file, datos)

    print(f"Usuario agregado: {nombre} (Normalizado: {nombre_normalizado})")  # 🔍 Log para depuración
    return jsonify({"mensaje": "Usuario agregado"}), 201

@app.route('/usuarios/<nombre>', methods=['GET'])
def obtener_usuario(nombre):
    """Obtiene la información de un usuario por su nombre normalizado"""
    datos = cargar_datos(db_file)
    nombre_normalizado = normalizar_texto(nombre)

    print(f"Buscando usuario: {nombre} (Normalizado: {nombre_normalizado})")  # 🔍 Log para depuración

    if nombre_normalizado not in datos:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(datos[nombre_normalizado])

@app.route('/usuarios/<nombre>', methods=['DELETE'])
def eliminar_usuario(nombre):
    """Elimina un usuario de la base de datos"""
    datos = cargar_datos(db_file)
    nombre_normalizado = normalizar_texto(nombre)

    print(f"Intentando eliminar: {nombre} (Normalizado: {nombre_normalizado})")  # 🔍 Log para depuración

    if nombre_normalizado not in datos:
        return jsonify({"error": "Usuario no encontrado"}), 404

    del datos[nombre_normalizado]
    guardar_datos(db_file, datos)
    return jsonify({"mensaje": "Usuario eliminado"}), 200

if __name__ == "__main__":
    app.run(debug=True)
