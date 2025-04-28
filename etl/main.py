import sys
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from etl.ingest_data import ingest_data
from etl.create_dimensions import create_dimensions
from etl.create_normalized import create_normalized_table
from etl.s3_utils import download_json_from_s3
from etl.pivot_data import pivot_data

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Definir BASE_DIR y ajustar la ruta para apuntar a la carpeta 'data' fuera de 'etl'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "laliga.db")
DOWNLOAD_PATH = os.path.join(BASE_DIR, "data", "laliga_2009_2010_matches.json")

def connect_to_sqlite():
    """Establecer conexión con la base de datos SQLite."""
    try:
        print(f"Ruta base: {BASE_DIR}")
        print(f"Ruta de la carpeta 'database': {DATABASE_DIR}")
        print(f"Ruta de la base de datos: {DATABASE_PATH}")

        # Crear la carpeta 'database' si no existe
        if not os.path.exists(DATABASE_DIR):
            os.makedirs(DATABASE_DIR)
            print(f"Carpeta 'database' creada en: {DATABASE_DIR}")
        else:
            print(f"La carpeta 'database' ya existe en: {DATABASE_DIR}")

        conn = sqlite3.connect(DATABASE_PATH)
        print(f"Conexión a SQLite exitosa. Base de datos creada en: {DATABASE_PATH}")
        return conn
    except Exception as e:
        print(f"Error al conectar a SQLite: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Configuración de S3 desde el archivo .env
    BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    OBJECT_KEY = os.getenv("OBJECT_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    print(f"BUCKET_NAME: {BUCKET_NAME}")
    print(f"OBJECT_KEY: {OBJECT_KEY}")
    print(f"DOWNLOAD_PATH: {DOWNLOAD_PATH}")

    # Crear la carpeta 'data' si no existe
    download_dir = os.path.dirname(DOWNLOAD_PATH)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Carpeta 'data' creada en: {download_dir}")

    # Descargar el archivo JSON desde S3
    download_json_from_s3(BUCKET_NAME, OBJECT_KEY, DOWNLOAD_PATH, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Conectar a SQLite
    conn = connect_to_sqlite()

    # Ejecutar el pipeline
    ingest_data(conn)
    create_dimensions(conn)
    create_normalized_table(conn)
    pivot_data(conn)

    # Cerrar la conexión
    conn.close()
    print("Pipeline ETL completado.")