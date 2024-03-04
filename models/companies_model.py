from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


class Companies(Base):
  __tablename__ = "companies"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  contact_email_address = Column(String)
  phone_number = Column(String, unique=True, index=True)
  user = relationship("User", secondary="user_company_table", back_populates="companies")
  films = relationship("Film", back_populates="company")
  timestamp = Column(DateTime)


class UserRoleEnum(Enum):
  writer = "writer"
  producer = "producer"
  director = "director"

# users and companies have a many to many relationship where the role is “owner” or “member”
user_company_table = Table(
  "user_company_association",
  Base.metadata,
  Column("user_id", ForeignKey("users.id")),
  Column("company_id", ForeignKey("companies.id")),
  Column('role', ENUM(UserRoleEnum))  # role is owner or member
)