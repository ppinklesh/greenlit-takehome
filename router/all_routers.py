from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db_connection import get_db
from router.schemas import UserBase, FilmBase, CompanyBase, AddFilmToUser
from controller.user_controller import UserController
from controller.film_controller import FilmController
from controller.company_controller import CompanyController

base_prefix = '/api/v1'

user_router = APIRouter(
  prefix=base_prefix,
  tags=['users']
)

@user_router.post('/create_user')
async def user(request: UserBase, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.create(request)

@user_router.post('/add_film_to_user')
async def add_film_to_user(request: AddFilmToUser, db: Session = Depends(get_db)):
  userController = UserController(db)
  return userController.add_film_to_user(request)

film_router = APIRouter(
  prefix=base_prefix,
  tags=['films']
)
@film_router.post('/create_films')
async def films(request: FilmBase, db: Session = Depends(get_db)):
  filmController = FilmController(db)
  return filmController.create(request)

company_router = APIRouter(
  prefix=base_prefix,
  tags=['companies']
)
@company_router.post('/create_company')
async def companies(request: CompanyBase, db: Session = Depends(get_db)):
  companyController = CompanyController(db)
  return companyController.create(request)