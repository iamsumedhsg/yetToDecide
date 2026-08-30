import sys
from pathlib import Path

# Add root & backend directory to sys.path to ensure seamless import resolution
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
BACKEND_DIR = BASE_DIR.parent

for path in (str(PROJECT_ROOT), str(BACKEND_DIR), str(BASE_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routes.health import router as health_router
from .routes.events import router as events_router
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI Backend for SIH Thermal Anomaly Source Attribution Dashboard"
)

# Enable CORS for frontend dashboard development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health_router)
app.include_router(events_router)

# Serve Frontend static assets and index.html
FRONTEND_DIR = PROJECT_ROOT / "frontend"
if (FRONTEND_DIR / "css").exists():
    app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
if (FRONTEND_DIR / "js").exists():
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")

@app.get("/")
def root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "Welcome to SIH Thermal Anomaly Attribution API",
        "docs": "/docs",
        "health": "/health",
        "events": "/events",
        "stats": "/events/stats",
        "geojson": "/events/geojson"
    }

