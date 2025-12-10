from flask import Flask, request, jsonify, render_template, redirect, url_for # Importa Flask y utilidades para manejar solicitudes, respuestas y plantillas
import psycopg2 # Importa el cliente de PostgreSQL para conectar y ejecutar consultas
from psycopg2.extras import RealDictCursor # Importa un cursor que devuelve filas como diccionarios
import traceback # Importa herramientas para mostrar trazas de error


app = Flask(__name__)

# Configuración DB
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


 # Tabla de recuperación

# Crea la tabla `recup_pass` en la base de datos si no existe
def crear_tabla():
    # Solicita una conexión a la base de datos
    conexion = conectar_bd()
    if conexion:
        # Crea un cursor para ejecutar la sentencia SQL
        cursor = conexion.cursor()
        # Ejecuta la sentencia SQL para crear la tabla
        cursor.execute("""
        CREATE TABLE restablecer (
            id SERIAL PRIMARY KEY,
            correo_electronico VARCHAR(100) NOT NULL,
            nueva_contraseña VARCHAR NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_usuarios INT NOT NULL REFERENCES registro (id_usuarios))
        """);
        # Inserta datos y cierra cursor y conexión
        conexion.commit()
        cursor.close()
        conexion.close()
        
# Ruta para mostrar el formulario de recuperación de contraseña
@app.route('/restablecer', methods=['GET'])
def restablecer():
    # Renderiza la plantilla restablecer.html`
    return render_template('restablecer.html')


# Procesamiento para verificar correo --------------------------------------------------------------------------------
@app.route('/verificar', methods=['POST'])
def verificar():

    correo_electronico = request.values.get('correo_electronico', '').strip()# Obtiene el correo electrónico del formulario y elimina espacios en blanco. El "values" se utiliza para que acepte todo tipo de información enviada sin importar su método

    if not correo_electronico: # Verifica que el correo no esté vacío
        return jsonify(error="Faltan datos obligatorios")

    conexion = conectar_bd() # Conecta a la base de datos
    if conexion is None:
        return jsonify(error="No se pudo conectar a la base de datos")

    cursor = conexion.cursor() # Crea un cursor para ejecutar consultas

    # Verificar que el correo exista en la tabla registro
    cursor.execute(
        "SELECT id_usuarios FROM registro WHERE correo_electronico = %s",
        (correo_electronico,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not usuario:
        return jsonify(error="El correo no existe en el sistema.")

    return jsonify(success=True, mensaje="El correo existe en el sistema. Por favor ingrese su nueva contraseña.")

# Ruta para cambiar la contraseña--------------------------------
@app.route('/cambiar', methods=['POST'])
def cambiar():

    correo_electronico = request.values.get('correo_electronico', '').strip()# Obtiene el correo electrónico del formulario y elimina espacios en blanco. El "values" se utiliza para que acepte todo tipo de información enviada sin importar su método
    nueva_contraseña = request.values.get('nueva_contraseña', '').strip()# Obtiene la nueva contraseña del formulario y elimina espacios en blanco. El "values" se utiliza para que acepte todo tipo de información enviada sin importar su método
    
    print("correo:", correo_electronico)
    print("nueva:", nueva_contraseña)

    if not correo_electronico or not nueva_contraseña:
        return jsonify(error="Faltan datos obligatorios")

    conexion = conectar_bd()
    if conexion is None:
        return jsonify(error="No se pudo conectar a la base de datos")

    cursor = conexion.cursor()

    # Verificar que el correo exista en la tabla registro
    cursor.execute(
        "SELECT id_usuarios FROM registro WHERE correo_electronico = %s",
        (correo_electronico,)
    )

    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conexion.close()
        return jsonify(error="El correo no existe en el sistema.")

    # Actualiza la contraseña
    cursor.execute(
        "UPDATE registro SET contraseña = %s WHERE correo_electronico = %s", # Actualiza la contraseña del usuario donde su correo sea igual al proporcionado
        (nueva_contraseña, correo_electronico)
    )

    id_usuarios = usuario[0] # Obtiene el id_usuarios del usuario encontrado

    # Guarda el evento en la tabla recuperacion
    cursor.execute(
        """
        INSERT INTO restablecer (correo_electronico, nueva_contraseña, id_usuarios)
        VALUES (%s, %s, %s)
        """,
        (correo_electronico, nueva_contraseña, id_usuarios)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(success=True)
