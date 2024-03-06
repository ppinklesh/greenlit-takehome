from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from router.schemas import UserBase, FilmBase, CompanyBase, AddFilmToUser, UserFilm
from models.user_model import User
from models.film_model import Film, user_film_table

class UserController:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, request: UserBase):
        
        if self.db.query(User).filter(User.email == request.email).first():
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        new_user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            minimun_fee=request.minimun_fee,
            timestamp=request.timestamp
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def add_film_to_user(self, request: AddFilmToUser):
        user = self.db.query(User).filter(User.id == request.user_id).first()
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        film = self.db.query(Film).filter(Film.id == request.film_id).first()
        if not film:          
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
        
        user_film = self.db.query(user_film_table).filter(user_film_table.c.user_id == request.user_id, user_film_table.c.film_id == request.film_id).first()
        if user_film:
            return {"message": f"User role in film already exists with the role {user_film.role.name}", 'status_code': status.HTTP_409_CONFLICT}
        
        user_film_data = {
            "user_id": request.user_id,
            "film_id": request.film_id,
            "role": request.role
        }
        self.db.execute(user_film_table.insert().values(user_film_data))
        self.db.commit()
        return {"message": "User role in film added successfully", 'status_code': status.HTTP_202_ACCEPTED}
    

    def get_user_films(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_films = []
        # user_film = self.db.query(user_film_table, Film).join(Film).filter(user_film_table.c.user_id == user_id).all()
        user_film = self.db.query(user_film_table, Film).filter(user_film_table.c.user_id == user_id).join(Film, user_film_table.c.film_id == Film.id).all()
        # user_film_data = (5, 1, 1, <UserRoleEnum.writer: 'writer'>, <models.film_model.Film object at 0x000001C9EC3E5DC0>)
        for result in user_film:
            user_film_schema = UserFilm(role=result[3].value, film=result[4])
            user_films.append(user_film_schema)
        return user_films

    def update_user_role(self, user_id, film_id, new_role):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        film = self.db.query(Film).filter(Film.id == film_id).first()
        if not film:          
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")

        if film not in user.film:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not associated with the specified film")

        user_film = self.db.query(user_film_table).filter(user_film_table.c.user_id == user_id, user_film_table.c.film_id == film_id).first()
        print(user_film)
        user_film[3].role = new_role.value   #facing error while updating the role
        self.db.add(user_film)
        self.db.commit()
        return {"message": f"User role in film updated to {new_role} successfully", 'status_code': status.HTTP_202_ACCEPTED}