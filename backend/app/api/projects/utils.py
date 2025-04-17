from pathlib import Path
from uuid import uuid4
from PIL import Image
import aiofiles
from fastapi import File, HTTPException, UploadFile, status

from app.api.projects.constants import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_IMAGE_MIME_TYPES,
)


def validate_image_file(file: UploadFile = File(...)) -> None:
    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Forbidden file type")

    extension = Path(file.filename).suffix
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Forbidden file extension")

    return file


async def upload_image_file(image_file: UploadFile = File(...)) -> str:
    validate_image_file(image_file)
    file_bytes = await image_file.read()

    upload_dir = Path("uploads/project_images")

    extension = Path(image_file.filename).suffix
    new_filename = f"{uuid4().hex}{extension}"
    image_path = str(upload_dir / new_filename)

    async with aiofiles.open(image_path, "wb") as f:
        await f.write(file_bytes)

    return image_path


def delete_file(path: str) -> None:
    path_to_delete = Path(path)
    if path_to_delete.exists() and path_to_delete.is_file():
        path_to_delete.unlink()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File to delete was not found.",
        )
