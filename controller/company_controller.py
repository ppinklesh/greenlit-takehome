from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import CompanyBase
from models.companies_model import Companies

class CompanyController:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, request: CompanyBase):
        
        if self.db.query(Companies).filter(Companies.name == request.name).first():
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Companies already exists")

        new_company = Companies(
            name=request.name,
            contact_email_address=request.contact_email_address,
            phone_number=request.phone_number,
            timestamp=request.timestamp
        )
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company
    
    def get_Companies(self):
        return self.db.query(Companies).first()
