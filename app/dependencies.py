from fastapi import Request, Depends
from sqlmodel import Session, select
from datetime import datetime, timezone

from .database.database import get_session
from .models.models import User, Session as UserSession

def get_current_user(request: Request, session: Session = Depends(get_session)) -> User | None:
    """Get current user from session"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    
    # Get session from database
    db_session = session.exec(select(UserSession).where(UserSession.id == session_id, UserSession.is_active == True)).first()
    if not db_session:
        return None
    
    # Convert timezone-naive datetime from database to timezone-aware for comparison
    expires_at = db_session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at < datetime.now(timezone.utc):
        return None
    
    # Get user from database
    user = session.exec(select(User).where(User.id == db_session.user_id, User.is_active == True)).first()
    return user
