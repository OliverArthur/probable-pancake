from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.domain.topic.entities.topic import Topic, TopicCreate
from app.domain.accounts.entities.user import UserCredentials
from app.application.topic.topic_services import TopicServices
from app.presentation.container import get_dependencies
from app.presentation.api.authentication.auth import get_current_user


router = APIRouter(default_response_class=JSONResponse)
repo = get_dependencies().topic_repo


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Topic)
def create_topic(
    topic: TopicCreate,
    current_user: UserCredentials = Depends(get_current_user),
):
    user_id = current_user.id
    return TopicServices.create(repo, user_id, topic)
