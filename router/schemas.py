from pydantic import BaseModel, EmailStr, constr, validator, conint
from typing import List
from datetime import datetime
from models.film_model import Film, UserRoleEnum

class UserBase(BaseModel):
  first_name: str 
  last_name: str
  email: EmailStr
  minimun_fee: conint(ge=0)
  timestamp: datetime = datetime.now()

class AddFilmToUser(BaseModel):
  user_id: int
  film_id: int
  role: UserRoleEnum

class FilmBase(BaseModel):
  id: int
  title: str
  description: str
  budget: str
  release_year: datetime
  genres: List[str]
  timestamp: datetime = datetime.now()
  class Config:
    from_attributes = True

class UserFilm(BaseModel):
  role: UserRoleEnum
  film: FilmBase
  class Config:
    arbitrary_types_allowed = True


class CompanyBase(BaseModel):
  name: str
  contact_email_address: EmailStr
  phone_number: constr(min_length=10, max_length=12)
  timestamp: datetime = datetime.now()


  # Ensure that the phone number contains only digits
  @validator('phone_number')
  def validate_phone_number(cls, v):
      if not v.isdigit():
          raise ValueError('Phone number must contain only digits')
      return v