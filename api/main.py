from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, get_db
from models import Base, User
from sqlalchemy.orm import Session
import os
from routers import auth, users


app = FastAPI()

# Include routers
app.include_router(auth.router, prefix='')
app.include_router(users.router, prefix='/users')

@app.get("/")
def health_check():
    return {"status": "healthy", "project": "API"}


# Create
# Read (get)
# Update
# Delete