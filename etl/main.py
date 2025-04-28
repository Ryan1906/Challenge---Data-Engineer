import sys
import os
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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subir un nivel
DOWNLOAD_PATH = os.path.join(BASE_DIR, "data", "laliga_2009_2010_matches.json")

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

    # Descargar el archivo JSON desde S3
    download_json_from_s3(BUCKET_NAME, OBJECT_KEY, DOWNLOAD_PATH, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Ejecutar el pipeline
    ingest_data()
    create_dimensions()
    create_normalized_table()
    pivot_data()