from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.infra.database.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.email
