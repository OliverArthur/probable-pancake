from typing import Protocol, List


from app.domain.topic.entities.topic import Topic, TopicCreate, TopicUpdate


class ITopicRepo(Protocol):
    """
    Topic Repository Interface
    """

    def get_all(
        self, page: int = 1, per_page: int = 10, search: str = ""
    ) -> List[Topic]:
        """
        Get all topics
        """
        ...

    def get_by_id(self, topic_id: int) -> Topic:
        """
        Get topic by id
        """
        ...

    def create(self, user_id: int, topic: TopicCreate) -> Topic:
        """
        Create new topic
        """
        ...

    def update(self, topic_id: int, topic: TopicUpdate) -> Topic:
        """
        Update topic
        """
        ...

    def delete(self, topic_id: int) -> None:
        """
        Delete topic
        """
        ...
