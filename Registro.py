from conexion import conectar

def registrar_usuario(identificacion, nombre, apellido, direccion, telefono, correo, mensaje):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO registro (identificacion, nombre, apellido, direccion, telefono, correo_electronico, mensaje)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    datos = (identificacion, nombre, apellido, direccion, telefono, correo, mensaje)

    cursor.execute(sql, datos)
    conn.commit()

    cursor.close()
    conn.close()

    print("Registro realizado correctamente.")