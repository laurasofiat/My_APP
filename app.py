from flask import Flask, render_template, request, jsonify, redirect, url_for # Importa la función `Flask` y utilidades para renderizar plantillas y manejar solicitudes
from conexion_registros import conectar_bd as conectar_bd_guardar # Importa función desde `conexion_registros`
from conexion_inicio import conectar_bd as conectar_bd_inicio # Importa la función `conectar_bd_inicio` desde `conexion_inicio`
from recup_pass import conectar_bd as conectar_bd_verificar  # Importa la función `conectar_bd_verificar` desde `recup_pass`
from recup_pass import conectar_bd as conectar_bd_cambiar  # Importa la función `conectar_bd_cambiar` desde `recup_pass`
import smtplib # Importa el módulo para enviar correos electrónicos usando SMTP
from email.message import EmailMessage # Importa clase para crear mensajes de correo electrónico


app = Flask(__name__)
# Crea la aplicación Flask usando el nombre del módulo actual

#Rutas----------------------------------------------------------------------------

# Página principal
@app.route('/')
def principal():
    # Devuelve la plantilla `index.html` para la ruta raíz
    return render_template('index.html')

# Registro
@app.route('/registro')
def registro():
    # Muestra el formulario de registro (`registro.html`)
    return render_template('registro.html')

# Iniciar sesión
@app.route('/inicio')
def login():
    # Muestra la página de inicio de sesión (`inicio.html`)
    return render_template('inicio.html')

# Enviar (declaración de salud o lo que sea en tu proyecto)
@app.route('/envia')
def enviar():
    # Renderiza la plantilla para enviar información (`envia.html`)
    return render_template('envia.html')

# Acerca de
@app.route('/acerca')
def acerca():
    # Página 'acerca' que muestra información sobre el sitio
    return render_template('acerca.html')

# Departamentos
@app.route('/dep')
def departamentos():
    # Muestra la vista de departamentos (`dep.html`)
    return render_template('dep.html')

# Seguros
@app.route('/seguros')
def seguros():
    # Página de información sobre seguros
    return render_template('seguros.html')

# Pagina de usuarios registrados o que iniciaron sesión
@app.route('/pagina_usuarios')
def pagina_usuarios():
    # Muestra la página de usuario registrada/iniciada (`pg_usuario.html`)
    return render_template('pg_usuario.html')

# Política de privacidad
@app.route('/politicas')
def politicas():
    # Muestra la política de privacidad
    return render_template('politica.html')

# Reserva
@app.route('/reservar')
def reservas():
    # Página para realizar reservas
    return render_template('reservar.html')

# Terminos
@app.route('/terminos')
def terminos():
    # Muestra los términos y condiciones
    return render_template('terminos.html')

# Contactos
@app.route('/contactos')
def contactos():
    # Página de contacto general
    return render_template('contacto.html')

#Página contactos para los usuarios
@app.route('/contactosR')
def contactosR():
    # Contacto para usuarios registrados
    return render_template('contacto_R.html')

#Página seguros para los usuarios
@app.route('/segurosR')
def segurosR():
    # Contacto para usuarios registrados
    return render_template('seguros_R.html')

#Página envía para los usuarios
@app.route('/enviaR')
def enviaR():
    # Versión de `envia` para usuarios registrados
    return render_template('envia_R.html')

#Página reservar para los registrados
@app.route('/reservarR')
def reservarR():
    # Versión de `reservar` para usuarios registrados
    return render_template('reservar_R.html')

# Página de recperación de contraseña para los registrados
@app.route('/restablecer')
def restablecer():
    # Muestra la página de recuperación de contraseña
    return render_template('restablecer.html')

# Prosesamiento para registrarse-----------------------------------------------------------------------------------------------------

@app.route('/guardar', methods=['POST'])
def guardar():
    # Obtiene los valores enviados desde el formulario `registro.html`
    primer_nombre = request.form.get('p_nombre', '').strip()
    segundo_nombre = request.form.get('s_nombre', '').strip()
    primer_apellido = request.form.get('p_apellido', '').strip()
    segundo_apellido = request.form.get('s_apellido', '').strip()
    contraseña = request.form.get('contraseña', '').strip()
    telefono = request.form.get('telefono', '').strip()
    correo_electronico = request.form.get('correo_electronico', '').strip()
    direccion = request.form.get('direccion', '').strip()
    mensaje = request.form.get('mensaje', '').strip()

    # Intenta conectar a la base de datos usando la función importada
    conexion = conectar_bd_guardar()
    if conexion is None:
        # Si falla la conexión devuelve el error en JSON
        return jsonify(error="No se pudo conectar a la base de datos")
    
    # Verificar contraseña duplicada
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuarios FROM registro WHERE contraseña = %s", (contraseña,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return jsonify(error="La contraseña ya está registrada. Intenta con otra.")

    # Verificar teléfono duplicado
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuarios FROM registro WHERE telefono = %s", (telefono,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return jsonify(error="El telefono ya está registrado. Intenta con otro.")
    
    # Verificar correo duplicado
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuarios FROM registro WHERE correo_electronico = %s", (correo_electronico,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return jsonify(error="El correo ya está registrado. Intenta con otro.")


    # Crea un cursor para ejecutar la inserción SQL
    sql_insertar = """
        INSERT INTO registro (p_nombre, s_nombre, p_apellido, s_apellido, contraseña, telefono, correo_electronico, direccion, mensaje)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Ejecuta la consulta con los parámetros obtenidos del formulario
    cursor.execute(sql_insertar, (primer_nombre,segundo_nombre, primer_apellido, segundo_apellido,
                                  contraseña, telefono, correo_electronico, direccion, mensaje))
    
    # Confirma la transacción en la base de datos
    conexion.commit()
    
    # Cierra el cursor y la conexión
    cursor.close()
    conexion.close()

    # Mensaje de confirmación para mostrar en JSON
    return redirect('/pagina_usuarios')

 # Prosesamiento de iniciar sesión---------------------------------------------------------------------------------------------------------------

@app.route('/procesar1', methods=['POST']) 
def procesar1(): # Nombre de la función que gestiona el inicio de sesión
    
    # Obtiene los datos enviados por el formulario de inicio de sesión
    contraseña = request.form.get('contraseña')
    correo_electronico = request.form.get('correo_electronico')

    # Valida que los campos obligatorios no estén vacíos
    if not contraseña or not correo_electronico:
        return jsonify(error="Faltan datos obligatorios")
    
    # Conectar a la base de datos
    conexion = conectar_bd_inicio()
    if conexion is None:
        return jsonify(error="No se pudo conectar a la base de datos")

    # Crea un cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Ejecuta la consulta para comprobar si existe el usuario con la contraseña y correo
    cursor.execute(
        "SELECT id_usuarios FROM registro WHERE contraseña=%s AND correo_electronico=%s",
        (contraseña, correo_electronico)
    )
    usuario = cursor.fetchone() #Obtiene el primer resultado de la consulta
    
    # Si no existe el usuario, cierra recursos y devuelve error en JSON
    if usuario is None:
        cursor.close()
        conexion.close()
        return jsonify(error="Usuario o contraseña incorrectos")

    # Extrae el id del usuario encontrado
    id_usuarios = usuario[0]
    
    # Inserta un registro de inicio de sesión en la tabla `inicio`
    cursor.execute(
        "INSERT INTO inicio (contraseña, correo_electronico,id_usuarios) VALUES (%s, %s, %s)",
        (contraseña, correo_electronico, id_usuarios)
    )
    
    # Confirma la inserción
    conexion.commit()

    # Cierra cursor y conexión
    cursor.close()
    conexion.close()

    # Mensaje de confirmación para mostrar en JSON
    return redirect('/pagina_usuarios')


# Procesamiento para RECUPERACIÓN de contraseña -----------------------------------------------------------------------------------------

# Procesamiento para verificar correo -------------------------
@app.route('/verificar', methods=['POST'])
def verificar():

    correo_electronico = request.values.get('correo_electronico', '').strip() # Obtiene el correo electrónico del formulario y elimina espacios en blanco. El "values" se utiliza para que acepte todo tipo de información enviada sin importar su método

    if not correo_electronico: # Verifica que el correo no esté vacío
        return jsonify(error="Faltan datos obligatorios")

    conexion = conectar_bd_verificar() # Conecta a la base de datos
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

    conexion = conectar_bd_cambiar()
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

if __name__=='__main__': #Ejecutas las rutas si se cumple la condición
    app.run(debug=True)