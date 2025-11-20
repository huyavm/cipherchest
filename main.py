import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, accounts, attachments, backup, dashboard, tools
from database.init_db import init_db
from utils.settings import get_settings
from security.rate_limiter import RateLimiter

settings = get_settings()
limiter = RateLimiter(settings.rate_limit)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")
app.include_router(attachments.router, prefix="/api")
app.include_router(backup.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(tools.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    os.makedirs(settings.attachments_dir, exist_ok=True)
    os.makedirs(settings.backup_dir, exist_ok=True)
    init_db()


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    return await limiter.middleware(request, call_next)


@app.get("/health")
async def health():
    return {"status": "ok"}
