from pydantic import BaseModel, EmailStr, constr, validator, conint
from typing import List
from datetime import datetime
from models.film_model import Film, UserRoleEnum
from models.companies_model import CompanyRoleEnum

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

class AddCompanyToUser(BaseModel):
  user_id: int
  company_id: int
  role: CompanyRoleEnum

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
  id: int
  name: str
  contact_email_address: EmailStr
  phone_number: constr(min_length=10, max_length=12)
  timestamp: datetime = datetime.now()

class UserCompany(BaseModel):
  role: CompanyRoleEnum
  company: CompanyBase
  class Config:
    arbitrary_types_allowed = True

