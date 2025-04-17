from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from .api.auth.router import router as auth_router
from .api.admins.router import router as admins_router
from .api.projects.router import router as projects_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    upload_dir = Path("uploads/project_images")
    upload_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://frontend:5173",
]  # ["*"] for public api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [auth_router, admins_router, projects_router]
for router in routers:
    app.include_router(router)


@app.get("/ping")
async def root():
    return {"success": True, "message": " pong"}
