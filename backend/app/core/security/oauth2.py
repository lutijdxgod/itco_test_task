from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db_helper as db
from ... import models
from app.schemas.token import Token, TokenData
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.auth.secret_key
ALGORITHM = settings.auth.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.access_token_expire_minutes


def create_access_token(data: dict):
    """
    Creates a new access token.

    Args:
        data: The data to encode into the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verifies the validity of an access token.

    Args:
        token: The JWT token to verify.
        credentials_exception: The exception to raise if verification fails.

    Returns:
        TokenData: The decoded token data.

    Raises:
        HTTPException: If the token is invalid or the user ID is missing.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(user_id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(
    token: Token = Depends(oauth2_scheme),
    db: AsyncSession = Depends(db.session_getter),
):
    """
    Retrieves the current authenticated user based on the provided token.

    Args:
        token: The JWT token provided by the user.
        db: The database session.

    Returns:
        models.User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user cannot be found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user_query = select(models.Administrator).where(
        models.Administrator.id == int(token.user_id)
    )
    query_result = await db.scalars(user_query)
    user = query_result.first()

    return user
