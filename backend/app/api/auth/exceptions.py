from fastapi import HTTPException, status


INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Invalid credentials",
)
