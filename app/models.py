from sqlalchemy import String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)  # pending|in_progress|done
    priority: Mapped[int] = mapped_column(Integer, default=3)  # 1-5
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    owner: Mapped["User"] = relationship("User", back_populates="tasks")
