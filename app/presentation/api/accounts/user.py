from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.application.account.register_user_services import RegisterUserServices
from app.application.account.get_user_services import GetUserServices
from app.domain.accounts.entities.user import User, UserCredentials
from app.presentation.container import get_dependencies

repo = get_dependencies().user_repo
router = APIRouter(default_response_class=JSONResponse)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(response: JSONResponse, credentials: UserCredentials):
    try:
        email = credentials.email.lower()
        user = await GetUserServices.get_user_by_credentials(email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )
        return await RegisterUserServices.register(repo, credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request"
        )
