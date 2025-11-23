from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "clave_secreta"  # necesario para usar flask

# conexión a la base de datos PostgreSQL
def conectar_bd():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Bases_de_datos_Proyecto",
            user="postgres",
            password="123456",
            port="5432"
        )
        return conn

    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


# ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':

        id_usuarios = request.form['id_usuarios']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo_electronico']
        mensaje = request.form['mensaje']

        conn = None
        try:
            conn = conectar_bd()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    '''
                    INSERT INTO formulario 
                    (id_usuarios, nombre, apellido, direccion, telefono, correo_electronico, mensaje)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (id_usuarios, nombre, apellido, direccion, telefono, correo, mensaje)
                )
                conn.commit()
                cur.close()

                flash('¡Datos registrados exitosamente!', 'success')
            else:
                flash('Error: No fue posible conectarse a la base de datos.', 'danger')

        except psycopg2.Error as e:
            flash(f'Error al insertar datos: {e}', 'danger')

        finally:
            if conn:
                conn.close()

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)