from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import UserBase, FilmBase, CompanyBase, AddFilmToUser
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
        
        # user_film = self.db.query(User.film).filter_by(id=request.film_id, user_id=request.user_id).first()
        user_film = self.db.query(user_film_table).filter_by(user_id = request.user_id, film_id = request.film_id).first()
        # print(request.role)  role is not getting updated
        if user_film:
            user_film.role = request.role
        else:
            user.film.append(film)
            user_film = user.film[-1]  
            user_film.role = request.role
        self.db.commit()
        return {"message": "User role in film added successfully", 'status_code': status.HTTP_202_ACCEPTED}
    
    def get_user(self):
        return self.db.query(User).first()