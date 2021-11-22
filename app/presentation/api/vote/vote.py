from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse


from app.application.vote.vote_services import VoteServices
from app.domain.accounts.entities.user import UserCredentials
from app.domain.vote.entities.vote import VoteCreate
from app.presentation.api.authentication.auth import get_current_user
from app.presentation.container import get_dependencies


repo = get_dependencies().vote_repo
post_repo = get_dependencies().posts_repo
router = APIRouter(default_response_class=JSONResponse)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteCreate,
    current_user: UserCredentials = Depends(get_current_user),
) -> dict:
    """
    Endpoint to vote for a posts
    """
    user_id = current_user.id
    direction = vote.direction
    post_id = vote.post_id
    VoteServices.vote(repo, post_repo, user_id, post_id, direction)

    message = "Voted successfully" if direction == 1 else "Vote removed successfully"

    return {"detail": message}
