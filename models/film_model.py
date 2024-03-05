from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum
from models.companies_model import Companies

class UserRoleEnum(Enum):
  writer = "writer"
  producer = "producer"
  director = "director"

# users and films have a many to many relationship where the role of the user can be either “writer”, “producer”, or “director”
user_film_table = Table(
  "user_film_association",
  Base.metadata,
  Column("id", Integer, primary_key=True, index=True),
  Column("user_id", ForeignKey("users.id"), index=True),
  Column("film_id", ForeignKey("film.id"), index=True),
  Column('role', ENUM(UserRoleEnum))  # Role can be 'writer', 'producer', or 'director' 
)
class Film(Base):
  __tablename__ = "film"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True, unique=True, nullable=False)
  description = Column(String)
  budget = Column(String)
  release_year = Column(DateTime)
  genres = Column(ARRAY(String))
  users = relationship("models.user_model.User", secondary=user_film_table, back_populates="film")
  company_id = Column(Integer, ForeignKey('companies.id'))
  companies = relationship("Companies", back_populates="film")
  timestamp = Column(DateTime)
