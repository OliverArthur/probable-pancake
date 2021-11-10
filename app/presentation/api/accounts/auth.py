from datetime import datetime, timedelta
from enum import Enum
from operator import attrgetter
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWSError, jwt
from pydantic import BaseModel

from app.core.config import get_settings
from app.domain.accounts.entities import User
from app.domain.accounts.services import user_service
from app.presentation.container import get_dependencies

_secret_key, _expire_minutes, _algorithm = attrgetter(
    "JWT_SECRET_KEY", "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "JWT_ALGORITHM"
)(get_settings())

repo = get_dependencies().user_repo


class TokenType(str, Enum):
    bearer = "bearer"


class Token(BaseModel):
    access_token: str
    expire: int
    token_type: TokenType = TokenType.bearer

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: Optional[int] = None
    is_active: Optional[bool] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(default_response_class=JSONResponse)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=_expire_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, _secret_key, algorithm=_algorithm)


def verify_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, _secret_key, algorithms=[_algorithm])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exceptions
        token_data = TokenData(user_id=user_id)
    except ExpiredSignatureError:
        raise credentials_exceptions
    except JWSError:
        raise credentials_exceptions
    return token_data



async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token(token, credentials_exceptions)
    user = await user_service.get_by_id(repo, token.user_id)
    return user