from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWSError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import TokenData

SECRET_KEY = "089af25bfa1690396aa44c2df15ad86353b7a09c08ae83e4912d3a380a523a7d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oath2_schema = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exceptions
        token_data = TokenData(user_id=user_id)
    except ExpiredSignatureError:
        raise credentials_exceptions
    except JWSError:
        raise credentials_exceptions
    return token_data


def get_current_user(
    token: str = Depends(oath2_schema),
    db: Session = Depends(get_db),
):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token(token, credentials_exceptions)

    return db.query(User).filter(User.id == token.user_id).first()
