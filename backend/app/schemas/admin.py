from datetime import datetime
from pydantic import (
    BaseModel,
)


class AdminCreate(BaseModel):
    username: str
    password: str


class AdminOut(BaseModel):
    id: int
    username: str
    created_at: datetime
