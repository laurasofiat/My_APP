from flask import Flask, request, jsonify, render_template, redirect, url_for #Importa Flask y utilidades para manejar peticiones y plantillas
import psycopg2 # Cliente PostgreSQL para conectar y ejecutar consultas
from psycopg2.extras import RealDictCursor # Cursor que puede devolver filas como diccionarios
import traceback # Módulo para mostrar trazas de error
import os # Módulo para utilizar funciones del sistema operativo
import datetime # Funciones para manejar fechas y horas
import uuid # Generador de identificadores únicos
import re #Módulo que sirve para validar formatos de texto


# Crea la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = { #DB_CONFIG es un diccionario que contiene los parámetros de conexión a la base de datos
    'host': 'localhost',
    'database': 'MedicAgenda',
    'user': 'postgres',
    'password': '123456',
    'port': 5432
}
# Diccionario con la configuración de la base de datos

# Función para conectar la base de datos
def conectar_bd():
    # Intenta establecer una conexión con PostgreSQL usando DB_CONFIG
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        return conexion
    except psycopg2.Error as e:
        # Imprime el error y devuelve None si no puede conectar
        print(f" Error al conectar a la base de datos: {e}")
        return None

# Tabla REGISTRO--------------------------------------------------------

# Crea la tabla `registro` si no existe
def crear_tabla():
    # Obtiene una conexión
    conexion = conectar_bd()
    if conexion:
        # Crea un cursor para ejecutar la sentencia SQL
        cursor = conexion.cursor()
        # Ejecuta la sentencia SQL para crear la tabla
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro (
            id_usuarios SERIAL NOT NULL PRIMARY KEY,
            p_nombre VARCHAR NOT NULL,
            s_nombre VARCHAR,
            p_apellido VARCHAR NOT NULL,
            s_apellido VARCHAR,
            contraseña VARCHAR(50) NOT NULL,
            telefono VARCHAR NOT NULL,
            correo_electronico VARCHAR NOT NULL,
            direccion VARCHAR NOT NULL,
            mensaje VARCHAR
        );
        """)
        # Confirma la operación y cierra recursos
        conexion.commit()
        cursor.close()
        conexion.close()

# Ruta para mostrar la página de registro
@app.route('/registro', methods=['GET'])
def registro():
    # Renderiza la plantilla `registro.html`
    return render_template('registro.html')

@app.route('/guardar', methods=['POST'])
def guardar(): 
    error=None #Muestra mensajes en pantalla
    try:
        # Obtiene una conexión a la base de datos
        conexion = conectar_bd()
        if conexion is None:
            # Devuelve error en la página si no se puede conectar
            return jsonify(error="Error: No se pudo conectar a la base de datos")
        
        # Lee los datos enviados por el formulario y los mantiene en la página (a excepción de contraseña y mensaje)
        primer_nombre = request.form.get('p_nombre', '').strip() #el strip elimina espacios al inicio y final de la cadena
        segundo_nombre = request.form.get('s_nombre', '').strip()
        primer_apellido = request.form.get('p_apellido', '').strip()
        segundo_apellido = request.form.get('s_apellido', '').strip()
        contraseña = request.form.get('contraseña', '').strip()
        telefono = request.form.get('telefono', '').strip()
        correo_electronico = request.form.get('correo_electronico', '').strip()
        direccion = request.form.get('direccion', '').strip()
        mensaje = request.form.get('mensaje', '').strip()

        # Valida que los campos obligatorios estén presentes
        if not primer_nombre or not primer_apellido or not direccion or not telefono or not correo_electronico:
            # Devuelve error si faltan datos obligatorios
            return jsonify(error="Faltan datos obligatorios")
        
        # Inserta datos de registro en la tabla `registro`
        cursor = conexion.cursor()
        sql_insertar = """
        INSERT INTO registro (p_nombre, s_nombre, p_apellido, s_apellido, contraseña, telefono, correo_electronico, direccion, mensaje)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Ejecuta la inserción con los parámetros, los inserta, cierra el cursor y la conexión
        cursor.execute(sql_insertar, (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, contraseña, telefono, correo_electronico, direccion, mensaje))
        conexion.commit()
        cursor.close()
        conexion.close()

        # Devuelve mensaje de éxito en JSON
        return jsonify(mensaje=f"¡Hola, {correo_electronico}! Registro guardado correctamente")
    
    except Exception as e:
        # Imprime el error y devuelve una respuesta JSON con el mensaje de error
        print("\n ERROR SQL:")
        print(e)
        traceback.print_exc()
        return jsonify(error="Error al procesar la solicitud")
