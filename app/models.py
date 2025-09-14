import string
from database import Base
from sqlalchemy import String, Integer, Column, DateTime
from datetime import datetime, timezone


class URL(Base):
    __tablename__ = 'url'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    unique = Column(String)
    link = Column(String)
    field = Column(String)
    created_at = Column(DateTime, default=lambda : datetime.now(timezone.utc))