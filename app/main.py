from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.files import router as files_router

setup_logging()

app = FastAPI(title="Secure Backend API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(files_router)


@app.get("/")
def home():
    return {"message": "Secure Backend API is running"}