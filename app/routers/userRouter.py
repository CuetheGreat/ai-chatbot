from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import DB
from app.schemas.user import User, UserCreate
from app.crud.user import get_user, get_user_by_email, create_user

router = APIRouter()

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(DB.get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(DB.get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
