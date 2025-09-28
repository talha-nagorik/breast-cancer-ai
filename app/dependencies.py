from fastapi import Request, Depends
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional

from .database.database import get_session
from .models.models import User, Session as UserSession

def get_current_user(request: Request, session: Session = Depends(get_session)) -> Optional[User]:
    """Get current user from session"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    
    # Get session from database
    db_session = session.exec(select(UserSession).where(UserSession.id == session_id, UserSession.is_active == True)).first()
    if not db_session or db_session.expires_at < datetime.utcnow():
        return None
    
    # Get user from database
    user = session.exec(select(User).where(User.id == db_session.user_id, User.is_active == True)).first()
    return user
