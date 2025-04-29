import sys
import psycopg2
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from etl.database import SessionLocal, engine
from etl.models import Base
from etl.ingest_data import ingest_data
from etl.create_dimensions import create_dimensions
from etl.create_normalized import create_normalized_table
from etl.pivot_data import pivot_data



# Load environment variables from .env file
load_dotenv()

# Route to the JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(BASE_DIR, "data", "laliga_2009_2010_matches.json")

if __name__ == "__main__":
    
    if os.path.exists("database/laliga.sqlite"):
        os.remove("database/laliga.sqlite")
        
    Base.metadata.create_all(bind=engine)

  
    BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    OBJECT_KEY = os.getenv("OBJECT_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    print(f"BUCKET_NAME: {BUCKET_NAME}")
    print(f"OBJECT_KEY: {OBJECT_KEY}")
    print(f"DOWNLOAD_PATH: {DOWNLOAD_PATH}")

   
    download_dir = os.path.dirname(DOWNLOAD_PATH)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Carpeta 'data' creada en: {download_dir}")

   
    from etl.sqlite.s3_utils import download_json_from_s3
    download_json_from_s3(BUCKET_NAME, OBJECT_KEY, DOWNLOAD_PATH, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    
    session = SessionLocal()

    try:
       
        ingest_data(session, DOWNLOAD_PATH)
        create_dimensions(session)
        create_normalized_table(session)
        pivot_data(session)
    finally:
      
        session.close()

    print("Pipeline ETL completed.")