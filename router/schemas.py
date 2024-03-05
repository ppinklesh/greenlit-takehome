from pydantic import BaseModel, EmailStr, constr, validator, conint
from typing import List
from datetime import datetime

class UserBase(BaseModel):
  first_name: str 
  last_name: str
  email: EmailStr
  minimun_fee: conint(ge=0)  
  timestamp: datetime = datetime.now()

class FilmBase(BaseModel):
  title: str
  description: str
  budget: str
  release_year: datetime
  genres: List[str]
  user: int
  company: int
  timestamp: datetime = datetime.now()

class CompanyBase(BaseModel):
  name: str
  contact_email_address: EmailStr
  phone_number: constr(min_length=10, max_length=12)
  user: int
  films: int
  timestamp: datetime = datetime.now()

  # Ensure that the phone number contains only digits
  @validator('phone_number')
  def validate_phone_number(cls, v):
      if not v.isdigit():
          raise ValueError('Phone number must contain only digits')
      return v