from pydantic import BaseModel


class ProjectOut(BaseModel):
    id: int
    title: str
    description: str | None
    image_url: str | None
