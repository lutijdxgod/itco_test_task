from datetime import datetime
from typing import Annotated

from sqlalchemy import (
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core.base import Base

str_not_nullable_an = Annotated[str, mapped_column(nullable=False)]
str_nullable_an = Annotated[str | None, mapped_column(nullable=True)]
int_not_nullable_an = Annotated[int, mapped_column(nullable=False)]
int_nullable_an = Annotated[int | None, mapped_column(nullable=True)]
datetime_now_not_nullable_an = Annotated[
    datetime,
    mapped_column(TIMESTAMP, nullable=False, server_default=func.now()),
]


class Administrator(Base):
    __tablename__ = "admins"

    username: Mapped[str_not_nullable_an]
    password: Mapped[str_not_nullable_an]
    created_at: Mapped[datetime_now_not_nullable_an]


class Project(Base):
    __tablename__ = "projects"

    title: Mapped[str_not_nullable_an]
    description: Mapped[str_nullable_an]
    image_path: Mapped[str_nullable_an]
