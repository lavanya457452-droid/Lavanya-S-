from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Create AI-generated five-panel comics with stories, images, and PDFs.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

app.include_router(router)