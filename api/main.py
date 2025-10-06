from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, get_db 
from models import Base, User
from security import get_password_hash
from sqlalchemy.orm import Session
import os
from routers import users, quizzes, submissions
from dotenv import load_dotenv

load_dotenv()

# Load environment variables with development defaults
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "dev_admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "dev_admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "dev_password")
PRODUCTION = os.getenv("PRODUCTION")

if PRODUCTION == "True":
    API_BASE = "http://api:8000"
else:
    API_BASE = "http://localhost:8000"



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
app.include_router(submissions.router, prefix='/submissions')


@app.get("/")
def health_check():
    return {"status": "healthy", "project": "API"}

@app.get("/mode")
def prod_or_dev():
    return PRODUCTION


# Quizzes endpoint

# post   http://localhost:8000/quizzes/          <--- create quiz
# get    http://localhost:8000/quizzes/          <--- get all
# get    http://localhost:8000/quizzes/{quiz_id} <--- get one quiz
# put    http://localhost:8000/quizzes/{quiz_id} <--- update one
# delete http://localhost:8000/quizzes/{quiz_id} <--- delete one


# Users endpoint

# post   http://localhost:8000/users/          <--- create user
# get    http://localhost:8000/users/          <--- get user
# get    http://localhost:8000/users/{quiz_id} <--- get one user
# put    http://localhost:8000/users/{quiz_id} <--- update one
# delete http://localhost:8000/users/{quiz_id} <--- delete one

# Submissions endpoint
# post   http://localhost:8000/users/          <--- Submit answers
