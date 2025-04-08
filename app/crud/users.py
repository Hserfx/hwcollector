from app.models.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, user_data: dict):
    existing_user = db.query(User).filter_by(id=user_data["id"]).first()
    if existing_user:
        return existing_user
    
    new_user = User(
        id=user_data["id"],
        email=user_data["email"],
        name=user_data["name"],
        given_name=user_data.get("given_name"),
        picture=user_data.get("picture")
    )
    
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        return db.query(User).filter_by(id=user_data["id"]).first()

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
