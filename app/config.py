# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") 
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

DB_USERNAME = os.getenv('DB_USERNAME')  
DB_PASSWORD = os.getenv('DB_PASSWORD')  
DB_HOST = os.getenv('DB_HOST')  
DB_PORT = os.getenv('DB_PORT')  
DB_NAME = os.getenv('DB_NAME')  

