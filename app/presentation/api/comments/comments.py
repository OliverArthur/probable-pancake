from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.application.comments.comments_services import CommentsService
from app.domain.accounts.entities.user import UserCredentials
from app.domain.comments.entities.comments import Comment, CommentCreate
from app.presentation.api.authentication.auth import get_current_user
from app.presentation.container import get_dependencies

repo = get_dependencies().comment_repo
router = APIRouter(default_response_class=JSONResponse)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    current_user: UserCredentials = Depends(get_current_user),
):
    """
    Create a comment
    """
    post_id = comment.post_id
    user_id = current_user.id
    return CommentsService.create_comment(repo, user_id, post_id, comment)
