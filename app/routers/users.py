from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from pydantic import BaseModel

from ..models.models import User, Session as UserSession
from ..auth import get_password_hash, verify_password
from ..database.database import get_session
from ..dependencies import get_current_user

# Pydantic models for JSON requests
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str
    confirm_password: str

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Signup page


@router.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request, user: User | None = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/dashboard")

    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": user
    })

# Login page


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, user: User | None = Depends(get_current_user)):
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
    existing_user = session.exec(
        select(User).where(User.email == email)).first()
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
    user = session.exec(select(User).where(
        User.email == email, User.is_active == True)).first()

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

# JSON API endpoints for AJAX requests
@router.post("/api/login")
async def api_login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    """JSON API endpoint for login"""
    # Get user from database
    user = session.exec(select(User).where(User.email == request.email, User.is_active == True)).first()
    
    if user and verify_password(request.password, user.password_hash):
        # Create new session
        user_session = UserSession(user_id=user.id)
        session.add(user_session)
        session.commit()
        session.refresh(user_session)

        response = JSONResponse(content={"success": True, "message": "Login successful"})
        response.set_cookie(key="session_id", value=user_session.id)
        return response
    else:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Invalid email or password"}
        )

@router.post("/api/signup")
async def api_signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
):
    """JSON API endpoint for signup"""
    # Basic validation
    if request.password != request.confirm_password:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Passwords do not match"}
        )

    if len(request.password) < 6:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Password must be at least 6 characters"}
        )

    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == request.email)).first()
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "User already exists with this email"}
        )

    # Create new user
    password_hash = get_password_hash(request.password)
    new_user = User(
        name=request.full_name,
        email=request.email,
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

    response = JSONResponse(content={"success": True, "message": "Account created successfully"})
    response.set_cookie(key="session_id", value=user_session.id)
    return response
