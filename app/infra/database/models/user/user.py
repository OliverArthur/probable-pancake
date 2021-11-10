from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.infra.database.sqlalchemy import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(TIMESTAMP(timezone=True), server_onupdate=text("now()"))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.email
