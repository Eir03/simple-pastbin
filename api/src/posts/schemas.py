from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    user_id: Optional[int]
    category_id: Optional[int] = Field(default=1)
    title: Optional[str]
    content: str
    is_public: Optional[bool] = Field(default=True)
    delete_after_reading: Optional[bool] = Field(default=False)
    tags: Optional[List[str]]
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# TODO сделать наследование, сюда написать общие поля, а там только уникальные
class PostRead(BaseModel):
    id: int
    title: Optional[str]
    blob_storage_url: str
    hash: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_public: bool
    delete_after_reading: bool
    tags: Optional[List[str]]
    content: Optional[str]

    class Config:
        from_attributes = True

class PostPublicRead(BaseModel):
    id: int
    hash: str
    title: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]
    tags: Optional[List[str]]
    is_public: bool

    class Config:
        from_attributes = True

class PostDetailRead(BaseModel):
    id: int
    hash: str
    title: Optional[str]
    content: str
    created_at: datetime
    expires_at: Optional[datetime]
    delete_after_reading: bool
    tags: Optional[List[str]]

    class Config:
        from_attributes = True
