from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional

from ..models.models import User, MedicalRecord, FamilyHistory
from ..database.database import get_session
from ..dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin")
async def admin_panel(request: Request, user: Optional[User] = Depends(get_current_user), session: Session = Depends(get_session)):
    """Admin panel - basic user management"""
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
