from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from app.infrastructure.database.base_class import Base


class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    
    author = relationship('User')
    posts = relationship('Posts')
    