from fastapi import APIRouter, Depends, File, UploadFile
import logging

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.file_service import save_file

logger = logging.getLogger("app")

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    filename = save_file(file)

    logger.info(
        "File uploaded by user: %s, filename: %s",
        current_user.username,
        filename
    )

    return {
        "message": "File uploaded successfully",
        "filename": filename
    }