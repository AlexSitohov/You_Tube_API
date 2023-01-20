import re
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from pydantic import validator

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-]+$")


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    date_time_registration: datetime

    @validator("username")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username should contains only letters"
            )
        return value

    class Config:
        orm_mode = True


class ContentCreate(BaseModel):
    title: str
    date_time_uploaded: datetime

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id_user: int
    is_staff: bool


class Like(BaseModel):
    content_id: int

    class Config:
        orm_mode = True


class PlayList(BaseModel):
    playlist_title: str
    date_time_created: datetime

    class Config:
        orm_mode = True


class PlayListResponse(BaseModel):
    id: int
    playlist_title: str
    date_time_created: datetime
    contents: list[ContentCreate]

    class Config:
        orm_mode = True


class AddContentToPlaylist(BaseModel):
    content_id: list[int]


class Subscription(BaseModel):
    youtuber_id: int

    class Config:
        orm_mode = True


class Profile(BaseModel):
    first_name: str
    last_name: str
    username: str

    @validator("username")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username should contains only letters"
            )
        return value

    class Config:
        orm_mode = True


class Comment(BaseModel):
    body: str
    content_id: int
    date_time_created: datetime

    class Config:
        orm_mode = True
