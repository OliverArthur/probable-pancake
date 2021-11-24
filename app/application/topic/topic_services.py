from abc import ABC

from fastapi import HTTPException, status

from app.domain.topic.interfaces.topic_repo import ITopicRepo
from app.domain.topic.entities.topic import TopicCreate, Topic


class TopicServices(ABC):
    """
    Topic services
    """

    @classmethod
    def create(
        cls, topic_repo: ITopicRepo, user_id: int, topic_data: TopicCreate
    ) -> Topic:
        """
        Create new topic
        :param topic_repo: topic repository interface
        :param user_id: user id
        :param topic_data: topic data
        :return:
        """
        try:
            new_topic = topic_repo.create(user_id, topic_data)

        except (Exception, AttributeError, TypeError) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return new_topic
