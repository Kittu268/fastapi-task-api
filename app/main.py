from fastapi import FastAPI
from .database import Base, engine
from .models import *  # noqa
from .routers import tasks, auth

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="A simple, documented REST API with FastAPI, SQLite, SQLAlchemy, and JWT auth."
)

@app.get("/", tags=["health"])
def root():
    return {"message": "✅ Task API is running. See /docs for Swagger UI."}

app.include_router(auth.router)
app.include_router(tasks.router)
