from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db_connection import get_db
from router.schemas import UserBase, FilmBase, CompanyBase


user_router = APIRouter(
  prefix='/api/v1',
  tags=['users']
)

@user_router.post('/create_user')
async def user(request: UserBase, db: Session = Depends(get_db)):
  return db_post.create(db, request)