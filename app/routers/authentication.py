from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.oauth2 import create_access_token
from app.schemas import Token
from app.utils import verify_password

router = APIRouter()


@router.post("/auth/login", tags=["authentication"], response_model=Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user
    """
    user = db.query(User).filter(User.email == data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"user_id": user.id, "is_active": user.is_active}
    )

    return {"access_token": access_token, "token_type": "bearer"}
