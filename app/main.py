from dataclasses import field
from re import I
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
import random
import string
from pydantic import BaseModel, field_validator
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from database import Base, create_tables, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from models import *
import validators


BASE62 = string.digits + string.ascii_letters

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class PostURL(BaseModel):
    id: int
    unique: str
    link: str

    field: str
    created_at: datetime

    
        
    
   

class GetURL(BaseModel):
    link: str

    @field_validator('link')
    def validate_link(cls, value):
        if len(value) < 1:
            raise HTTPException("Enter url to get short url")

        if not validators.url(value):
            raise HTTPException("Invalid url")

        return value

        
        


def encode(num: int) -> str:
    '''Function to encode a int into base62'''
    try:
        if num == 0:
            return BASE62[0]

        res = []
        while num > 0:
            res.append(BASE62[num%62])
            num//=62
        return "".join(reversed(res))

    except Exception as e:
        return "".join([random.choice(BASE62) for _ in range(5)])
        
def decode(code: str) -> int:
    '''Function to decode base62 string in int'''
    try:
        num = 0
        for c in code:
            num = num*62 + BASE62.index(c)
        return num

    except Exception as e:
        print(e)


@app.post('/links', tags=['URL'])
def input_link(link:GetURL, db:db_dependency):
    try:
        record = db.query(URL).filter(URL.link == link.link).first()
        if record:
            raise HTTPException(status_code=401, detail=f"URL is already present in the database: short url is http://short/{record.unique}")
        record = db.query(URL).order_by(URL.id.desc()).first()
     
        if record:
            i = record.id
            i += 1
        else:
            i = 0
        unique_code = encode(i)
        print(link.link)
        record = URL(
            unique = unique_code,
            link  = link.link

        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return {
            'id': record.id,
            'short_url': f"http://short/{record.unique}",
            'long_url': record.link}
    except HTTPException as e:
        print(e)
        return {
            'Error': e
        }

       


@app.get('/links/long', tags=['URL'])
def get_long_url(short_link: str, db: db_dependency):
    try:
        code = short_link.replace("http://short/", "")
        decoded = decode(code)
        record = db.query(URL).filter(URL.id == decoded).first()

        return {
            "long_url": record.link
        }
    except Exception as e:
        print(e)
        return {
            "error": "Not able to get short url"
        }


     
