from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.infrastructure.database.base_class import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    published = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    topic_id = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")
    topic = relationship("Topic")

    def __init__(
        self, title, content, owner_id, topic_id, published=False, image_url=None
    ):
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.topic_id = topic_id
        self.published = published
        self.image_url = image_url

    def __repr__(self):
        return "<Post %r>" % self.title
