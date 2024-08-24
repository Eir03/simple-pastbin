# models.py
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
    expires_at: Optional[datetime]

class PostRead(BaseModel):
    id: int
    title: Optional[str]
    content: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_public: bool
    delete_after_reading: bool
    tags: Optional[List[str]]

    class Config:
        orm_mode = True
