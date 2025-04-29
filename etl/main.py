import sys
import psycopg2
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from etl.sqlite.ingest_data import ingest_data
from etl.sqlite.create_dimensions import create_dimensions
from etl.sqlite.create_normalized import create_normalized_table
from etl.sqlite.s3_utils import download_json_from_s3
from etl.sqlite.pivot_data import pivot_data

from etl.Postgre.ingest_data_postgres import ingest_data_postgres
from etl.Postgre.create_dimensions_postgres import create_dimensions_postgres
from etl.Postgre.create_normalized_table_postgres import create_normalized_table_postgres


load_dotenv()

# Configuration of paths and database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "laliga.sqlite")
DOWNLOAD_PATH = os.path.join(BASE_DIR, "data", "laliga_2009_2010_matches.json")


def connect_to_postgres():
  
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("ProstgreSQL connection successful.")
        return conn
    except Exception as e:
        print(f"Error connecting to Postgresql {e}")
        sys.exit(1)


def connect_to_sqlite():
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        print(f"Sqlite Connection Succesfuly completed: {DATABASE_PATH}")
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Load environment variables
    BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    OBJECT_KEY = os.getenv("OBJECT_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    print(f"BUCKET_NAME: {BUCKET_NAME}")
    print(f"OBJECT_KEY: {OBJECT_KEY}")
    print(f"DOWNLOAD_PATH: {DOWNLOAD_PATH}")

    # Create the data directory if it doesn't exist
    download_dir = os.path.dirname(DOWNLOAD_PATH)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Carpeta 'data' creada en: {download_dir}")

    # Download the JSON file from S3
    download_json_from_s3(BUCKET_NAME, OBJECT_KEY, DOWNLOAD_PATH, AWS_ACCESS_KEY, AWS_SECRET_KEY)


    use_postgres = os.getenv("USE_POSTGRES", "false").lower() == "true"

    # Connect to the database
if use_postgres:
    conn = connect_to_postgres()


    ingest_data_postgres(conn)
    create_dimensions_postgres(conn)
    create_normalized_table_postgres(conn)
else:
    conn = connect_to_sqlite()
    ingest_data(conn)
    create_dimensions(conn)
    create_normalized_table(conn)
    pivot_data(conn)

    # Cerrar la conexión
    conn.close()
    print("Pipeline ETL completado.")