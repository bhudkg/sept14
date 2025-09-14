from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = 'sqlite:///./database.db'

engine = create_engine(
    url=DATABASE_URL, 
    connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)


