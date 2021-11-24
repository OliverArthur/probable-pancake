from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.application.account import AccountServices
from app.domain.accounts.entities.user import User, UserCredentials, UserUpdateMe
from app.presentation.api.authentication.auth import get_current_user
from app.presentation.container import get_dependencies

repo = get_dependencies().user_repo
router = APIRouter(default_response_class=JSONResponse)


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(response: JSONResponse, credentials: UserCredentials):
    return AccountServices.register_user(repo, credentials)


@router.put("/me", response_model=User, status_code=status.HTTP_200_OK)
def update_me(
    response: JSONResponse,
    user: UserUpdateMe,
    current_user: UserCredentials = Depends(get_current_user),
):
    return AccountServices.update_me(repo, user, current_user)


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
def get_me(
    response: JSONResponse,
    current_user: UserCredentials = Depends(get_current_user),
) -> User:
    return AccountServices.get_me(repo, current_user)
