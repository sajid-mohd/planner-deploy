from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from sqlalchemy.orm import Session

from .users import services as user_services
from .dependencies import get_db

router = APIRouter(tags=["web"])

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get("/login", response_class=HTMLResponse)
async def read_login(
    request: Request,
    error: Optional[str] = Query(None)
):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error}
    )


@router.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get("/verify-email", response_class=HTMLResponse)
async def read_verify_email(
    request: Request,
    email: str,
    db: Session = Depends(get_db)
):
    user = user_services.get_user_by_email(
        db,
        email=email
    )

    if not user:
        return RedirectResponse(url="/register")

    if user.is_email_verified:
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        request=request,
        name="verify_email.html",
        context={"email": email}
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@router.get("/analytics", response_class=HTMLResponse)
async def read_analytics(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={}
    )


@router.get("/momentum", response_class=HTMLResponse)
async def momentum_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="momentum.html",
        context={}
    )


@router.get("/tafakur", response_class=HTMLResponse)
async def tafakur_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tafakur.html",
        context={}
    )
