from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from datetime import datetime, timezone

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
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not user:
        return RedirectResponse(url="/signup")

    try:
        # Try to get JSON data first (for AJAX requests)
        try:
            json_data = await request.json()
            record_type = json_data.get("type")
            record_date = json_data.get("date")
            record_doctor = json_data.get("doctor")
            record_notes = json_data.get("notes", "")
            record_status = json_data.get("status", "pending")
        except:
            # Fallback to form data (for regular form submissions)
            form_data = await request.form()
            record_type = form_data.get("record_type") or form_data.get("type")
            record_date = form_data.get("record_date") or form_data.get("date")
            record_doctor = form_data.get("record_doctor") or form_data.get("doctor")
            record_notes = form_data.get("record_notes") or form_data.get("notes", "")
            record_status = form_data.get("status", "pending")

        # Validate required fields
        if not record_type or not record_date or not record_doctor:
            if request.headers.get("content-type", "").startswith("application/json"):
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="Missing required fields")
            else:
                return RedirectResponse(url="/dashboard?error=missing_fields", status_code=303)

        # Create new record
        new_record = MedicalRecord(
            user_id=user.id,
            date=record_date,
            type=record_type,
            result="Pending",
            doctor=record_doctor,
            notes=record_notes,
            status=record_status,
            status_color="#f59e0b" if record_status == "pending" else "#10b981"
        )

        session.add(new_record)
        session.commit()

        # Return appropriate response based on request type
        if request.headers.get("content-type", "").startswith("application/json"):
            from fastapi.responses import JSONResponse
            return JSONResponse(content={"success": True, "message": "Record added successfully"})
        else:
            return RedirectResponse(url="/dashboard", status_code=303)

    except Exception as e:
        if request.headers.get("content-type", "").startswith("application/json"):
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"Failed to add record: {str(e)}")
        else:
            return RedirectResponse(url="/dashboard?error=add_failed", status_code=303)

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
    user.updated_at = datetime.now(timezone.utc)

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
    user.updated_at = datetime.now(timezone.utc)

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
