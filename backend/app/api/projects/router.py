from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    Response,
    UploadFile,
    status,
    HTTPException,
)
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.projects.utils import delete_file, upload_image_file
from app.schemas.project import ProjectOut
from app.core.database import db_helper as db
from app import models
from app.api.projects.exceptions import PROJECT_NOT_FOUND
from app.core.security.oauth2 import get_current_user
from app.schemas.admin import AdminOut


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=list[ProjectOut], status_code=status.HTTP_200_OK)
async def get_projects(
    request: Request,
    db: AsyncSession = Depends(db.session_getter),
    current_user: AdminOut = Depends(get_current_user),
):
    projects_query = select(models.Project).order_by(models.Project.id.asc())
    projects = (await db.scalars(projects_query)).all()
    project_list = []

    for project in projects:
        image_url = None
        if project.image_path:
            filename = Path(project.image_path).name
            image_url = str(request.base_url) + f"static/project_images/{filename}"

        project_list.append(
            ProjectOut(
                id=project.id,
                title=project.title,
                description=project.description,
                image_url=image_url,
            )
        )

    return project_list


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_project(
    title: str = Form(...),
    description: str | None = Form(None),
    image_file: UploadFile | None = File(None),
    db: AsyncSession = Depends(db.session_getter),
    current_user: AdminOut = Depends(get_current_user),
):
    image_path: str | None = None
    if image_file:
        image_path = await upload_image_file(image_file)

    db.add(
        models.Project(
            title=title,
            description=description,
            image_path=image_path,
        )
    )
    await db.commit()

    return Response(
        status_code=status.HTTP_201_CREATED, content="Successfully created a project."
    )


@router.get("/{id}", response_model=ProjectOut)
async def get_project_by_id(
    request: Request,
    id: int = Path(),
    db: AsyncSession = Depends(db.session_getter),
    current_user: AdminOut = Depends(get_current_user),
):
    project_query = select(models.Project).where(models.Project.id == id)
    project = (await db.scalars(project_query)).first()

    if not project:
        raise PROJECT_NOT_FOUND

    image_url = None
    if project.image_path:
        filename = Path(project.image_path).name
        image_url = str(request.base_url) + f"static/project_images/{filename}"

    return ProjectOut(
        id=project.id,
        title=project.title,
        description=project.description,
        image_url=image_url,
    )


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_project(
    id: int = Path(),
    title: str | None = Form(None),
    description: str | None = Form(None),
    image_file: UploadFile | None = File(None),
    db: AsyncSession = Depends(db.session_getter),
    current_user: AdminOut = Depends(get_current_user),
):
    project_query = select(models.Project).where(models.Project.id == id)
    project = (await db.scalars(project_query)).first()
    if not project:
        raise PROJECT_NOT_FOUND

    if not any((title, description, image_file)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to change at least one field.",
        )

    new_info = {}

    if title:
        new_info["title"] = title

    if description:
        new_info["description"] = description

    image_path: str | None = None
    if image_file:
        if project.image_path:
            delete_file(project.image_path)

        image_path = await upload_image_file(image_file)
        new_info["image_path"] = image_path

    update_query = (
        update(models.Project).where(models.Project.id == id).values(**new_info)
    )
    await db.execute(update_query)
    await db.commit()

    return Response(
        status_code=status.HTTP_200_OK, content="Succesfully updated a project."
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: int,
    db: AsyncSession = Depends(db.session_getter),
    current_user: AdminOut = Depends(get_current_user),
):
    query = select(models.Project).where(models.Project.id == id)
    project = (await db.scalars(query)).first()

    if not project:
        raise PROJECT_NOT_FOUND

    if project.image_path:
        delete_file(project.image_path)

    await db.delete(project)
    await db.commit()
