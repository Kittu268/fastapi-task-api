from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

# -------- Auth --------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# -------- Tasks --------
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: str = Field(default="pending")
    priority: int = Field(default=3, ge=1, le=5)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        allowed = {"pending", "in_progress", "done"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None):
        if v is None:
            return v
        allowed = {"pending", "in_progress", "done"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v

class TaskOut(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
