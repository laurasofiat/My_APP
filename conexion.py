import psycopg2

def conectar():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            dbname="Bases de datos_Proyecto"
        )
        return conexion
    except Exception as error:
        print("Error al conectar:", error)
        return None