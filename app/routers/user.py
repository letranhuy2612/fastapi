from fastapi import APIRouter, Depends

from ..utils import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from app.models.models import  User


router = APIRouter()


@router.get('/me', response_model=schemas.UserResponse)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(User).filter(User.id == user_id).first()
    return user

