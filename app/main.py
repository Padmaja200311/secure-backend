from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.logging_config import setup_logging
from app.database.connection import get_db
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.files import router as files_router

setup_logging()

app = FastAPI(
    title="Secure Backend API",
    version="1.0.0",
    description="Secure FastAPI backend with JWT authentication, RBAC, file uploads, logging, testing, and Dockerization."
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(files_router)


@app.get("/")
def home():
    return {
        "message": "Secure Backend API is running"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }