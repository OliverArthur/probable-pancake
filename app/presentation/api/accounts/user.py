from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.application.account import AccountServices
from app.domain.accounts.entities.user import User, UserCredentials
from app.presentation.container import get_dependencies

repo = get_dependencies().user_repo
router = APIRouter(default_response_class=JSONResponse)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(response: JSONResponse, credentials: UserCredentials):
    try:
        user = AccountServices.get_user_by_credentials(repo, credentials)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists."
            )
        return AccountServices.register_user(repo, credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request"
        )
