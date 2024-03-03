from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime

class DBCompanies(Base):
  __tablename__ = "companies"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  contact_email_address = Column(String)
  phone_number = Column(String, unique=True, index=True)
  timestamp = Column(DateTime)