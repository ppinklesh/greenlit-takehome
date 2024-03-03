from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime

class DBFilm(Base):
  __tablename__ = "film"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  email = Column(String, unique=True, index=True)
  budget = Column(String)
  release_year = Column(DateTime)
  genres = Column(DateTime)
  timestamp = Column(DateTime)
