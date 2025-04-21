import logging

from fastapi import (
    FastAPI,
    Request,
)

from api import router as api_router
from api.redirect_views import router as redirect_views_router
from app_lifespan import lifespan
from core import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

app = FastAPI(
    title="URL Shortener",
    description="Opisanie",
    lifespan=lifespan,
)
app.include_router(api_router)
app.include_router(redirect_views_router)


@app.get("/")
def read_root(request: Request, name: str = "World"):
    docs_url = request.url.replace(path="/docs", query="")
    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }
