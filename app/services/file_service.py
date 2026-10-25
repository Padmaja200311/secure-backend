import os
import uuid

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf"
}


def save_file(file: UploadFile):
    extension = os.path.splitext(file.filename or "")[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    file_data = file.file.read()

    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    unique_filename = f"{uuid.uuid4()}{extension}"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    return unique_filename