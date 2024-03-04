from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


class Film(Base):
  __tablename__ = "film"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  email = Column(String, unique=True, index=True)
  budget = Column(String)
  release_year = Column(DateTime)
  genres = Column(ARRAY(String))
  user = relationship("User", secondary="user_film_table", back_populates="films")
  company = relationship("Company", back_populates="films")
  timestamp = Column(DateTime)

# Define enum for roles
class UserRoleEnum(Enum):
  writer = "writer"
  producer = "producer"
  director = "director"

# users and films have a many to many relationship where the role of the user can be either “writer”, “producer”, or “director”
user_film_table = Table(
  "user_film_association",
  Base.metadata,
  Column("user_id", ForeignKey("users.id")),
  Column("film_id", ForeignKey("film.id")),
  Column('role', ENUM(UserRoleEnum))  # Role can be 'writer', 'producer', or 'director' 
)
