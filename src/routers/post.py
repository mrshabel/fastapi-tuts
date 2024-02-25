from .. import models, utils, schemas
from ..database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Post Endpoints"])

@router.get("/", response_model=list[schemas.PostResponse]) 
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=201, response_model=schemas.PostResponse)
def create_test(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    return {"data": post}

@router.delete("/{id}", status_code=200)
def delete_post(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    print(post)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}

@router.put("/{id}", status_code=200)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()
    if not updated_post:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    query.update(dict(post), synchronize_session=False)
    db.commit()
    
    return {"data": query.first(), "message": "Post successfully updated"}