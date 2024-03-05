from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String, nullable=False)
  last_name = Column(String)
  email = Column(String, unique=True, index=True, nullable=False)
  minimun_fee = Column(Integer)
  films = relationship("Film", secondary="user_film_table", back_populates="users")
  company = relationship("Companies", secondary="user_company_table", back_populates="user")
  timestamp = Column(DateTime)
