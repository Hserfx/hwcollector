from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.users import get_users
from app.db.database import get_db

router = APIRouter()

@router.get('/')
def read_users(db: Session = Depends(get_db)):
    return get_users(db=db)
