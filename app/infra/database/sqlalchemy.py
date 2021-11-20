from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import get_settings

_SETTINGS = get_settings()

engine = create_engine(_SETTINGS.DB_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

db = scoped_session(SessionLocal)
