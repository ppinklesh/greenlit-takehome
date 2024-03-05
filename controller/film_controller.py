from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import FilmBase
from models.film_model import Film

class FilmController:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, request: FilmBase):
        if self.db.query(Film).filter(Film.title == request.title).first():
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Film already exists")

        new_film = Film(
            title=request.title,
            description=request.description,
            budget=request.budget,
            release_year=request.release_year,
            genres=request.genres,
            timestamp=request.timestamp
        )
        self.db.add(new_film)
        self.db.commit()
        self.db.refresh(new_film)
        return new_film
    
    def get_user(self):
        return self.db.query(Film).first()
