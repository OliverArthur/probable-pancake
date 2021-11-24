from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.application.account import AccountServices
from app.domain.accounts.entities.user import (User, UserCredentials,
                                               UserUpdateMe)
from app.presentation.api.authentication.auth import get_current_user
from app.presentation.container import get_dependencies

repo = get_dependencies().user_repo
router = APIRouter(default_response_class=JSONResponse)


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(response: JSONResponse, credentials: UserCredentials):
    try:
        user = AccountServices.verify_user_by_credentials(repo, credentials)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )
        return AccountServices.register_user(repo, credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request"
        )


@router.put("/me", response_model=User, status_code=status.HTTP_200_OK)
def update_me(
    response: JSONResponse,
    user: UserUpdateMe,
    current_user: UserCredentials = Depends(get_current_user),
):
    try:
        return AccountServices.update_me(repo, user, current_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
def get_me(
    response: JSONResponse,
    current_user: UserCredentials = Depends(get_current_user),
) -> User:
    return AccountServices.get_me(repo, current_user)
