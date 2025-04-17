from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.exceptions import INVALID_CREDENTIALS
from app.core.security import oauth2
from app.core.security.password import hash_password, verify_hashes
from app.schemas.admin import (
    AdminCreate,
)
from app.schemas.token import Token
from app.core.database import db_helper as db
from app.models import Administrator

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_credentials: AdminCreate,
    db: AsyncSession = Depends(db.session_getter),
):
    """
    Register a new user.

    Args:
        db: Database session dependency. Defaults to Depends(db.session_getter).

    Body Parameters:
        username: User's nickname.
        password: User's password.

    Returns:
        Response: Information about a newly created user with status code 201,
        or raises an HTTPException with status code 403 if a user with the given username already exists.
    """
    user_query = select(Administrator).filter(
        Administrator.username == user_credentials.username
    )
    user_query_result = await db.scalars(user_query)
    user = user_query_result.first()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is already a user with given username.",
        )

    hashed_password = hash_password(user_credentials.password)

    new_user = user_credentials.model_dump()
    user_credentials.password = hashed_password

    new_user = Administrator(**user_credentials.model_dump())
    db.add(new_user)
    await db.commit()

    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/login", response_model=Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db.session_getter),
):
    """
    Authenticate a user.

    Args:
        user_credentials: User's credentials provided via form data.
        db: Database session dependency.

    Form Data:
        username: User's nickname.
        password: User's password.

    Returns:
        dict: A dictionary containing the access token, token type, and user ID.

    Raises:
        INVALID_CREDENTIALS: If the username or password is incorrect.
    """
    user_query = select(Administrator).filter(
        Administrator.username == user_credentials.username
    )
    user_query_result = await db.scalars(user_query)
    user = user_query_result.first()

    if not user:
        raise INVALID_CREDENTIALS

    if not verify_hashes(user_credentials.password, user.password):
        raise INVALID_CREDENTIALS

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
    }
