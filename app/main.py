# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from . import models, database
from .web_router import router as web_router
from .api_router import router as api_router
from .analytics.router import router as analytics_router
from .tafakur.router import router as tafakur_router
from .config import settings

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Trust Railway's reverse proxy — makes request.base_url return https://
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://web-production-d51c5.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include routers
app.include_router(web_router)
app.include_router(api_router)
app.include_router(analytics_router)
app.include_router(tafakur_router, prefix="/api")
