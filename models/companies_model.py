from models.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


class CompanyRoleEnum(Enum):
  owner = "owner"
  member = "member"

# users and companies have a many to many relationship where the role is “owner” or “member”
user_company_table = Table(
  "user_company_association",
  Base.metadata,
  Column("id", Integer, primary_key=True, index=True),
  Column("user_id", ForeignKey("users.id"), index=True),
  Column("company_id", ForeignKey("companies.id"), index=True),
  Column('role', ENUM(CompanyRoleEnum))  # role is owner or member
)

class Companies(Base):
  __tablename__ = "companies"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True, unique=True, nullable=False)
  contact_email_address = Column(String)
  phone_number = Column(String)
  users = relationship("models.user_model.User", secondary=user_company_table, back_populates="companies")
  film = relationship("models.film_model.Film", back_populates="companies")
  timestamp = Column(DateTime)
