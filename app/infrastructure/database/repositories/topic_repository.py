from fastapi import HTTPException, status

from app.domain.topic.entities.topic import Topic, TopicCreate
from app.infrastructure.database.models.topic import Topic as TopicModel

from app.infrastructure.database.sqlalchemy import db


def create(user_id: int, topic: TopicCreate) -> Topic:
    new_topic = TopicModel(
        user_id=user_id,
        title=topic.title,
        description=topic.description,
    )

    if len(topic.title) == 0 or len(topic.description) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and description are required",
        )

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic
