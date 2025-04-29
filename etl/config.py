import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path configuration
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
DATABASE_FOLDER = os.path.join(os.getcwd(), 'database')
DB_PATH = os.getenv("DB_PATH", "etl/laliga.db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "laliga")
DB_USER = os.getenv("DB_USER", "laliga_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "laliga_pass")

# S3 configuration
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_OBJECT_KEY = os.getenv('S3_OBJECT_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
