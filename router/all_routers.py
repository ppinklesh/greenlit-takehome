from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db_connection import get_db
from router.schemas import UserBase, FilmBase, CompanyBase, AddFilmToUser, UserFilm, AddCompanyToUser, UserCompany
from controller.user_controller import UserController
from controller.film_controller import FilmController
from controller.company_controller import CompanyController
from models.film_model import UserRoleEnum
from models.companies_model import CompanyRoleEnum

base_prefix = '/api/v1'

user_router = APIRouter(prefix=base_prefix,tags=['users'])

@user_router.post('/create_user')
async def user(request: UserBase, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.create(request)

@user_router.post('/add_film_to_user')
async def add_film_to_user(request: AddFilmToUser, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.add_film_to_user(request)

@user_router.get("/get_user_films/{user_id}", response_model=list[UserFilm])
async def get_user_films(user_id: int, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.get_user_films(user_id)

@user_router.put("/user/{user_id}/film/{film_id}/role")
async def update_user_film_role(user_id: int, film_id: int, new_role: UserRoleEnum, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.update_user_role(user_id, film_id, new_role)

@user_router.post('/add_company_to_user')
async def get_company_to_user(request: AddCompanyToUser, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.add_company_to_user(request)

@user_router.get("/get_user_companies/{user_id}", response_model=list[UserCompany])
async def get_user_companies(user_id: int, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.get_user_companies(user_id)

@user_router.put("/user/{user_id}/company/{company_id}/role")
async def update_user_film_role(user_id: int, company_id: int, new_role: CompanyRoleEnum, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.update_user_company_role(user_id, company_id, new_role)

film_router = APIRouter(prefix=base_prefix,tags=['films'])

@film_router.post('/create_films')
async def films(request: FilmBase, db: Session = Depends(get_db)):
  filmController = FilmController(db)
  return filmController.create(request)


company_router = APIRouter(prefix=base_prefix,tags=['companies'])

@company_router.post('/create_company')
async def companies(request: CompanyBase, db: Session = Depends(get_db)):
  companyController = CompanyController(db)
  return companyController.create(request)