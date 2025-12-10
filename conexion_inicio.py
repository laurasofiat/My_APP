from flask import Flask, request, jsonify, render_template, redirect, url_for # Importa Flask y utilidades para manejar solicitudes, respuestas y plantillas
import psycopg2 # Importa el cliente de PostgreSQL para conectar y ejecutar consultas
from psycopg2.extras import RealDictCursor # Importa un cursor que devuelve filas como diccionarios
import traceback # Importa herramientas para mostrar trazas de error


# Crea la aplicación Flask
app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'MedicAgenda',
    'user': 'postgres',
    'password': '123456',
    'port': 5432
}
# Diccionario con la configuración de conexión a la base de datos

# Función para conectar la base de datos
def conectar_bd():
    # Intenta conectar a PostgreSQL usando la configuración proporcionada
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        return conexion
    except psycopg2.Error as e:
        # Imprime el error y devuelve None si la conexión falla
        print(f" Error al conectar a la base de datos: {e}")
        return None


 # Tabla Inicio

# Crea la tabla `inicio` en la base de datos si no existe
def crear_tabla():
    # Solicita una conexión a la base de datos
    conexion = conectar_bd()
    
    if conexion:
        # Crea un cursor para ejecutar la sentencia SQL
        cursor = conexion.cursor()
        # Ejecuta la sentencia SQL para crear la tabla
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inicio (
            id_inicio SERIAL NOT NULL PRIMARY KEY,
            contraseña VARCHAR(50) NOT NULL,
            correo_electronico VARCHAR NOT NULL,
            fecha TIMESTAMP DEFAULT NOW(),
            id_usuarios INT NOT NULL REFERENCES registro (id_usuarios)
        );
        """)
        # Inserta datos y cierra cursor y conexión
        conexion.commit()
        cursor.close()
        conexion.close()

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/inicio', methods=['GET'])
def inicio():
    # Renderiza la plantilla `inicio.html`
    return render_template('inicio.html')

@app.route('/procesar1', methods=['POST'])
def procesar1():
    error=None #Muestra mensajes en pantalla    
    # Procesa el formulario enviado desde la vista de inicio
    try:
        # Obtiene una conexión a la base de datos
        conexion = conectar_bd()
        if conexion is None:
            # Devuelve un mensaje de error en JSON si no se puede conectar
            return jsonify(error="No se pudo conectar a la base de datos")

        # Obtiene valores del formulario
        contraseña = request.form.get('contraseña', '').strip() #el strip elimina espacios al inicio y final de la cadena
        correo_electronico = request.form.get('correo_electronico', '').strip()
        id_usuarios = request.form.get('id_usuarios', '').strip()

        # Verifica que los campos obligatorios estén presentes
        if not contraseña or not correo_electronico:
            return jsonify(error="Faltan datos obligatorios")

        # Inserta un registro en la tabla `inicio`
        cursor = conexion.cursor()
        sql_insertar = """
        INSERT INTO inicio (contraseña, correo_electronico, id_usuarios)
        VALUES ( %s, %s, %s)
        """

        # Ejecuta la consulta con los parámetros obtenidos, los inserta, cierra cursor y conexión
        cursor.execute(sql_insertar, (contraseña, correo_electronico, id_usuarios))
        conexion.commit()
        cursor.close()
        conexion.close()

        # Devuelve mensaje de éxito en JSON
        return jsonify(mensaje=f"¡Hola, {correo_electronico}! Inicio guardado correctamente")

    except Exception as e:
        # Imprime el error
        print("\n ERROR SQL:")
        print(e)
        traceback.print_exc()
        return jsonify(error="Error al procesar la solicitud")
