import psycopg2

def conectar_bd():
    return psycopg2.connect(
    'host': 'localhost',
    'database': 'MedicAgenda',
    'user': 'postgres',
    'password': '123456',
    'port': 5432
    )   