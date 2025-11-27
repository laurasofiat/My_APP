from flask import Flask, render_template, request
from conexion_base_datos import conectar_bd

app = Flask(__name__)

# Página principal
@app.route('/')
def principal():
    return render_template('index.html')

# Registro
@app.route('/registro')
def registro():
    return render_template('registro.html')

# Iniciar sesión
@app.route('/inicio')
def login():
    return render_template('inicio.html')

# Enviar (declaración de salud o lo que sea en tu proyecto)
@app.route('/envia')
def enviar():
    return render_template('envia.html')

# Acerca de
@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

# Departamentos
@app.route('/dep')
def departamentos():
    return render_template('dep.html')

# Seguros
@app.route('/seguros')
def seguros():
    return render_template('seguros.html')

# Pagina de usuarios registrados o que iniciaron sesión
@app.route('/pagina_usuarios')
def pagina_de_usuarios():
    return render_template('pg_usuario.html')

# Política de privacidad
@app.route('/politicas')
def politicas():
    return render_template('politica.html')

# Reserva
@app.route('/reservar')
def reservas():
    return render_template('reservar.html')

# Contactos
@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

# Contactos
@app.route('/contactos')
def contactos():
    return render_template('contacto.html')

# Procesar formulario

@app.route('/procesar', methods=['POST'])
def procesar():
    id_usuarios = request.form.get('id_usuarios')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    correo_electronico = request.form.get('correo_electronico')
    mensaje = request.form.get('mensaje')

    conexion = conectar_bd()
    if conexion is None:
        return "Error: No se pudo conectar a la base de datos", 500

    cursor = conexion.cursor()
    sql_insertar = """
        INSERT INTO registro (id_usuarios, nombre, apellido, direccion, telefono, correo_electronico, mensaje)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_insertar, (id_usuarios, nombre, apellido, direccion, telefono, correo_electronico, mensaje))
    conexion.commit()
    cursor.close()
    conexion.close()

    mensaje = f"¡Hola, {nombre}! Registro guardado correctamente."
    return render_template('index.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)

