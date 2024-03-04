import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
# SQLALCHEMY_DATABASE_URL = os.getenv('db_url')
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://zdkzwsovjgltsqoabfej:123456789i8uytrdszxcvbnmui76tgfhjkiu7654e3wsedrtyuiu7654321234567890okmjiuyfdtgc@aws-0-ap-southeast-1.pooler.supabase.com:5432/greenlit_crud'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
 
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
 
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()