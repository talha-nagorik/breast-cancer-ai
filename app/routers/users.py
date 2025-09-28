from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime

from ..models.models import User, MedicalRecord, FamilyHistory, Session as UserSession
from ..auth import get_password_hash, verify_password
from ..database.database import get_session
from ..dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Signup page
@router.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request, user: Optional[User] = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/dashboard")

    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": user
    })

# Login page
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, user: Optional[User] = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/dashboard")

    return templates.TemplateResponse("login.html", {
        "request": request,
        "user": user
    })

# Handle signup form submission
@router.post("/signup")
async def signup_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    session: Session = Depends(get_session)
):
    # Basic validation
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Passwords do not match",
            "form_data": {"full_name": full_name, "email": email}
        })

    if len(password) < 6:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Password must be at least 6 characters",
            "form_data": {"full_name": full_name, "email": email}
        })

    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "User already exists with this email",
            "form_data": {"full_name": full_name, "email": email}
        })

    # Create new user
    password_hash = get_password_hash(password)
    new_user = User(
        name=full_name,
        email=email,
        password_hash=password_hash,
        age=0,
        phone="",
        emergency_contact="",
        blood_type="O+",
        allergies="",
        medications=""
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Create session
    user_session = UserSession(user_id=new_user.id)
    session.add(user_session)
    session.commit()
    session.refresh(user_session)

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_id", value=user_session.id)
    return response

# Handle login form submission
@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    # Get user from database
    user = session.exec(select(User).where(User.email == email, User.is_active == True)).first()
    
    if user and verify_password(password, user.password_hash):
        # Create new session
        user_session = UserSession(user_id=user.id)
        session.add(user_session)
        session.commit()
        session.refresh(user_session)

        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="session_id", value=user_session.id)
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password",
            "form_data": {"email": email}
        })

# Logout
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response
