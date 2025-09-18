from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, get_db 
from models import Base, User
from security import get_password_hash
from sqlalchemy.orm import Session
import os
from routers import users
from routers import quizzes # <-- la till denna raden

# Load environment variables with development defaults
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "dev_admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "dev_admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "dev_password")
PRODUCTION = os.getenv("PRODUCTION", "false").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Create initial admin user
    db: Session = next(get_db())
    try:
        # Create admin user if not exists
        admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not admin:
            hashed_password = get_password_hash(ADMIN_PASSWORD)
            admin = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=hashed_password,
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Startup error: {str(e)}")
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(users.router, prefix='/users')
app.include_router(quizzes.router, prefix='/quizzes') # <-- la till denna

@app.get("/")
def health_check():
    return {"status": "healthy", "project": "API"}
