import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_PATH')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')