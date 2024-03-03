from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime

class DBUser(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String)
  last_name = Column(String)
  email = Column(String, unique=True, index=True)
  minimun_fee = Column(String)
  timestamp = Column(DateTime)