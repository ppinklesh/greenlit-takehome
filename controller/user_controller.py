from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from router.schemas import UserBase, FilmBase, CompanyBase, AddFilmToUser, UserFilm, AddCompanyToUser, UserCompany
from models.user_model import User
from models.film_model import Film, user_film_table
from models.companies_model import Companies, user_company_table

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
        user_film = self.db.query(user_film_table, Film).filter(user_film_table.c.user_id == user_id).join(Film, user_film_table.c.film_id == Film.id).all()
        for result in user_film:
            user_film_schema = UserFilm(role=result[3].value, film=result[4])
            user_films.append(user_film_schema)
        return user_films

    def update_user_film_role(self, user_id, film_id, new_role):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        film = self.db.query(Film).filter(Film.id == film_id).first()
        if not film:          
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")

        if film not in user.film:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not associated with the specified film")

        user_film = (update(user_film_table).where(user_film_table.c.user_id == user_id, user_film_table.c.film_id == film_id).values(role = new_role.value))
        self.db.execute(user_film)
        self.db.commit()
        
        return {"message": f"User role in film updated to {new_role.value} successfully", 'status_code': status.HTTP_202_ACCEPTED}

    def add_company_to_user(self, request: AddCompanyToUser):
        user = self.db.query(User).filter(User.id == request.user_id).first()
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        company = self.db.query(Companies).filter(Companies.id == request.company_id).first()
        if not company:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Companies not found")
        
        user_company = self.db.query(user_company_table).filter(user_company_table.c.user_id == request.user_id, user_company_table.c.company_id == request.company_id).first()
        if user_company:
            return {"message": f"User role in company already exists with the role {user_company.role.name}", 'status_code': status.HTTP_409_CONFLICT}
        
        user_comapny_data = {
            "user_id": request.user_id,
            "company_id": request.company_id,
            "role": request.role
        }
        self.db.execute(user_company_table.insert().values(user_comapny_data))
        self.db.commit()
        return {"message": "User role in company added successfully", 'status_code': status.HTTP_202_ACCEPTED}
    
    def get_user_companies(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_companies = []
        user_company = self.db.query(user_company_table, Companies).filter(user_company_table.c.user_id == user_id).join(Companies, user_company_table.c.company_id == Companies.id).all()
        for result in user_company:
            company_data = {
                'id': result[4].id,
                'name': result[4].name,
                'contact_email_address': result[4].contact_email_address,
                'phone_number' : result[4].phone_number,
            }
            user_company_schema = UserCompany(role=result[3].value, company=company_data)
            user_companies.append(user_company_schema)
        return user_companies

    def update_user_company_role(self, user_id, company_id, new_role):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        company = self.db.query(Companies).filter(Companies.id == company_id).first()
        if not company:          
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        if company not in user.companies:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not associated with the specified company")

        user_company = (update(user_company_table).where(user_company_table.c.user_id == user_id, user_company_table.c.company_id == company_id).values(role = new_role.value))
        self.db.execute(user_company)
        self.db.commit()

        return {"message": f"User role in company updated to {new_role.value} successfully", 'status_code': status.HTTP_202_ACCEPTED}
    
