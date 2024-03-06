from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum
from models.companies_model import Companies, user_company_table
from models.film_model import Film, user_film_table


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String, nullable=False)
  last_name = Column(String)
  email = Column(String, unique=True, index=True, nullable=False)
  minimun_fee = Column(Integer)
  film = relationship("Film", secondary=user_film_table, back_populates="users")
  companies = relationship("Companies", secondary=user_company_table, back_populates="users")
  timestamp = Column(DateTime)
