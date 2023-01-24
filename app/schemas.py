import re
from fastapi import HTTPException, status, File, UploadFile
from pydantic import BaseModel, Field
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


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    date_time_registration: datetime

    class Config:
        orm_mode = True


class ContentCreate(BaseModel):
    title: str
    file: UploadFile = File(...)
    date_time_uploaded: datetime

    class Config:
        orm_mode = True


class ContentResponse(BaseModel):
    id: int
    title: str
    file: str = File(...)
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


class LikeResponse(BaseModel):
    content_id: int
    user_id: int

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
    contents: list[ContentResponse]

    class Config:
        orm_mode = True


class AddContentToPlaylist(BaseModel):
    playlist_id: int
    content_id: list[int]

    class Config:
        orm_mode = True


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


class ContentResponseWithCommentsAndLike(BaseModel):
    id: int
    title: str
    file: str = File(...)
    date_time_uploaded: datetime
    likes: list[LikeResponse]
    comments: list[Comment]

    class Config:
        orm_mode = True


class Wallet(BaseModel):
    balance: int = Field(ge=0)
    date_time_created: datetime

    class Config:
        orm_mode = True


class MakeTransaction(BaseModel):
    value: int = Field(ge=0)
    wallet_id_to: int


class Check(BaseModel):
    value: int
    date_time_created: datetime
    wallet_id_to: int

    class Config:
        orm_mode = True
