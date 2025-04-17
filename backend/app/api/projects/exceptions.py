from fastapi import HTTPException, status


PROJECT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Project not found.",
)
