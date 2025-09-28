from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from ..models.models import User
from ..database.database import get_session
from ..dependencies import get_current_user

router = APIRouter(
    tags=["Administration"],
    responses={404: {"description": "Not found"}}
)
templates = Jinja2Templates(directory="templates")


@router.get("/admin",
            response_class=HTMLResponse,
            summary="Admin Panel",
            description="Administrative panel for user management and system administration")
async def admin_panel(request: Request, user: User | None = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Admin panel - basic user management.

    Provides administrative interface for managing users and system settings.
    Requires authentication.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Get all users (basic admin functionality)
    users = session.exec(select(User)).all()

    context = {
        "request": request,
        "user": user,
        "users": users
    }

    return templates.TemplateResponse("admin.html", context)
