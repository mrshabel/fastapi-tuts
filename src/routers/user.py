from .. import models, schemas, utils
from ..database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["User Endpoints"])

@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    current_user = db.query(models.User).filter(models.User.id == id).first()
    print(current_user)
    if not current_user:
        raise HTTPException(status_code=404, detail="No user with such ID found")
    return current_user