from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from datetime import datetime

from ..models.models import User, MedicalRecord, FamilyHistory
from ..database.database import get_session
from ..dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dashboard page
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: User | None = Depends(get_current_user), session: Session = Depends(get_session)):
    if not user:
        return RedirectResponse(url="/signup")

    # Get user's medical records and family history
    medical_records = session.exec(select(MedicalRecord).where(MedicalRecord.user_id == user.id)).all()
    family_history = session.exec(select(FamilyHistory).where(FamilyHistory.user_id == user.id)).all()

    # Convert to dict format for template compatibility
    medical_records_dict = []
    for record in medical_records:
        medical_records_dict.append({
            "id": record.id,
            "date": record.date,
            "type": record.type,
            "result": record.result,
            "doctor": record.doctor,
            "notes": record.notes,
            "status": record.status,
            "status_color": record.status_color
        })

    family_history_dict = []
    for member in family_history:
        family_history_dict.append({
            "relation": member.relation,
            "age": member.age,
            "condition": member.condition
        })

    # Calculate stats
    completed_records = len([r for r in medical_records_dict if r["status"] == "completed"])
    pending_records = len([r for r in medical_records_dict if r["status"] == "pending"])
    total_doctors = len(set(r["doctor"] for r in medical_records_dict))

    # Recent activities (last 3 records)
    recent_activities = medical_records_dict[:3]

    context = {
        "request": request,
        "user": user,
        "stats": {
            "total_records": len(medical_records_dict),
            "completed_records": completed_records,
            "pending_records": pending_records,
            "total_doctors": total_doctors
        },
        "recent_activities": recent_activities,
        "medical_records": medical_records_dict,
        "family_history": family_history_dict
    }

    return templates.TemplateResponse("dashboard.html", context)

# Add medical record
@router.post("/add_record")
async def add_record(
    request: Request,
    record_type: str = Form(...),
    record_date: str = Form(...),
    record_doctor: str = Form(...),
    record_notes: str = Form(...),
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not user:
        return RedirectResponse(url="/signup")

    # Create new record
    new_record = MedicalRecord(
        user_id=user.id,
        date=record_date,
        type=record_type,
        result="Pending",
        doctor=record_doctor,
        notes=record_notes,
        status="pending",
        status_color="#f59e0b"
    )

    session.add(new_record)
    session.commit()

    return RedirectResponse(url="/dashboard", status_code=303)

# Update profile
@router.post("/update_profile")
async def update_profile(
    request: Request,
    full_name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    emergency_contact: str = Form(...),
    blood_type: str = Form(...),
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not user:
        return RedirectResponse(url="/signup")

    # Update user data
    user.name = full_name
    user.age = age
    user.email = email
    user.phone = phone
    user.emergency_contact = emergency_contact
    user.blood_type = blood_type
    user.updated_at = datetime.now(datetime.timezone.utc)

    session.add(user)
    session.commit()

    return RedirectResponse(url="/dashboard", status_code=303)

# Update medical info
@router.post("/update_medical_info")
async def update_medical_info(
    request: Request,
    allergies: str = Form(...),
    medications: str = Form(...),
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not user:
        return RedirectResponse(url="/signup")

    # Update medical info
    user.allergies = allergies
    user.medications = medications
    user.updated_at = datetime.now(datetime.timezone.utc)

    session.add(user)
    session.commit()

    return RedirectResponse(url="/dashboard", status_code=303)

# Add family member
@router.post("/add_family_member")
async def add_family_member(
    request: Request,
    relation: str = Form(...),
    age: int = Form(...),
    condition: str = Form(...),
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not user:
        return RedirectResponse(url="/signup")

    # Add family member
    new_member = FamilyHistory(
        user_id=user.id,
        relation=relation,
        age=age,
        condition=condition
    )

    session.add(new_member)
    session.commit()

    return RedirectResponse(url="/dashboard", status_code=303)

# Remove family member
@router.post("/remove_family_member")
async def remove_family_member(
    request: Request,
    index: int = Form(...),
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not user:
        return RedirectResponse(url="/signup")

    # Get family history records
    family_history = session.exec(select(FamilyHistory).where(FamilyHistory.user_id == user.id)).all()
    
    # Remove family member by index
    if 0 <= index < len(family_history):
        member_to_remove = family_history[index]
        session.delete(member_to_remove)
        session.commit()

    return RedirectResponse(url="/dashboard", status_code=303)

# API endpoints for AJAX requests
@router.get("/api/stats")
async def get_stats(request: Request, user: User | None = Depends(get_current_user), session: Session = Depends(get_session)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    medical_records = session.exec(select(MedicalRecord).where(MedicalRecord.user_id == user.id)).all()
    completed_records = len([r for r in medical_records if r.status == "completed"])
    pending_records = len([r for r in medical_records if r.status == "pending"])
    total_doctors = len(set(r.doctor for r in medical_records))

    return {
        "total_records": len(medical_records),
        "completed_records": completed_records,
        "pending_records": pending_records,
        "total_doctors": total_doctors
    }
