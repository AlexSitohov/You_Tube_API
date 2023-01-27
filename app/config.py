import os

from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
