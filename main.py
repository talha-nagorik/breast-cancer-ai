from typing import Union, Optional
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
from datetime import datetime, date

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# In-memory storage (replace with database in production)
users_db = {}
sessions_db = {}
medical_records_db = {}
family_history_db = {}

# Sample data
sample_user = {
    "id": "123456",
    "name": "Jane Doe",
    "email": "jane.doe@email.com",
    "age": 45,
    "phone": "+1 (555) 123-4567",
    "emergency_contact": "John Doe (+1 555-987-6543)",
    "blood_type": "O+",
    "allergies": "None",
    "medications": "Vitamin D, Calcium supplements"
}

sample_medical_records = [
    {
        "id": 1,
        "date": "2024-01-15",
        "type": "Mammogram",
        "result": "Normal",
        "doctor": "Dr. Sarah Johnson",
        "notes": "Routine screening - no abnormalities detected",
        "status": "completed",
        "status_color": "#10b981"
    },
    {
        "id": 2,
        "date": "2023-12-10",
        "type": "Ultrasound",
        "result": "Follow-up required",
        "doctor": "Dr. Michael Chen",
        "notes": "Small cyst detected - monitoring recommended",
        "status": "pending",
        "status_color": "#f59e0b"
    }
]

sample_family_history = [
    {"relation": "Mother", "condition": "Breast Cancer", "age": 52},
    {"relation": "Sister", "condition": "None", "age": 42},
    {"relation": "Grandmother", "condition": "Breast Cancer", "age": 68}
]

# Initialize sample data
users_db["jane.doe@email.com"] = sample_user
medical_records_db["123456"] = sample_medical_records
family_history_db["123456"] = sample_family_history

# Dependency to get current user
def get_current_user(request: Request):
    # In a real app, you'd check session/cookie
    # For demo purposes, we'll use a simple session check
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions_db:
        user_email = sessions_db[session_id]
        if user_email in users_db:
            return users_db[user_email]
    return None

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_current_user(request)
    
    # Sample data for the home page
    context = {
        "request": request,
        "user": user,
        "stats": {
            "accuracy_rate": 99.2,
            "lives_saved": "10K+"
        },
        "about_cards": [
            {
                "icon": "🎯",
                "title": "What is Breast Cancer?",
                "description": "Breast cancer is a disease in which cells in the breast grow out of control. It can start in different parts of the breast and can spread to other parts of the body."
            },
            {
                "icon": "📊",
                "title": "Prevalence",
                "description": "Breast cancer is the most common cancer among women worldwide, affecting 1 in 8 women during their lifetime. Early detection is crucial for successful treatment."
            },
            {
                "icon": "🔬",
                "title": "Our Technology",
                "description": "Using cutting-edge artificial intelligence and machine learning algorithms, our system provides accurate, non-invasive breast cancer detection."
            }
        ],
        "symptoms": [
            {"icon": "🔴", "title": "Lump or Mass", "description": "A new lump or mass in the breast or underarm area"},
            {"icon": "🔄", "title": "Shape Changes", "description": "Changes in breast size, shape, or appearance"},
            {"icon": "💧", "title": "Nipple Discharge", "description": "Clear or bloody discharge from the nipple"},
            {"icon": "🔴", "title": "Skin Changes", "description": "Redness, dimpling, or puckering of breast skin"},
            {"icon": "😣", "title": "Pain", "description": "Breast pain or tenderness that doesn't go away"},
            {"icon": "🔄", "title": "Nipple Changes", "description": "Nipple turning inward or changing position"}
        ],
        "detection_steps": [
            {"number": 1, "title": "Upload Images", "description": "Upload your mammogram or ultrasound images securely"},
            {"number": 2, "title": "AI Analysis", "description": "Our AI algorithms analyze the images for abnormalities"},
            {"number": 3, "title": "Expert Review", "description": "Results are reviewed by certified radiologists"},
            {"number": 4, "title": "Detailed Report", "description": "Receive comprehensive results and recommendations"}
        ],
        "risk_factors": [
            {
                "title": "Non-Modifiable Factors",
                "factors": [
                    "Age (risk increases with age)",
                    "Family history of breast cancer",
                    "Genetic mutations (BRCA1, BRCA2)",
                    "Personal history of breast cancer",
                    "Dense breast tissue"
                ]
            },
            {
                "title": "Modifiable Factors",
                "factors": [
                    "Physical inactivity",
                    "Alcohol consumption",
                    "Obesity after menopause",
                    "Hormone replacement therapy",
                    "Not having children or late pregnancy"
                ]
            }
        ]
    }
    return templates.TemplateResponse("home.html", context)

# Signup/Login page
@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard")
    
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": user
    })

# Handle signup form submission
@app.post("/signup")
async def signup_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
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
    if email in users_db:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "User already exists with this email",
            "form_data": {"full_name": full_name, "email": email}
        })
    
    # Create new user
    user_id = str(uuid.uuid4())[:6]
    new_user = {
        "id": user_id,
        "name": full_name,
        "email": email,
        "age": 0,
        "phone": "",
        "emergency_contact": "",
        "blood_type": "O+",
        "allergies": "",
        "medications": ""
    }
    
    users_db[email] = new_user
    medical_records_db[user_id] = []
    family_history_db[user_id] = []
    
    # Create session
    session_id = str(uuid.uuid4())
    sessions_db[session_id] = email
    
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_id", value=session_id)
    return response

# Handle login form submission
@app.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    # In a real app, you'd verify the password hash
    if email in users_db:
        # Create session
        session_id = str(uuid.uuid4())
        sessions_db[session_id] = email
        
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="session_id", value=session_id)
        return response
    else:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Invalid email or password",
            "form_data": {"email": email}
        })

# Dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/signup")
    
    # Get user's medical records and family history
    medical_records = medical_records_db.get(user["id"], [])
    family_history = family_history_db.get(user["id"], [])
    
    # Calculate stats
    completed_records = len([r for r in medical_records if r["status"] == "completed"])
    pending_records = len([r for r in medical_records if r["status"] == "pending"])
    total_doctors = len(set(r["doctor"] for r in medical_records))
    
    # Recent activities (last 3 records)
    recent_activities = medical_records[:3]
    
    context = {
        "request": request,
        "user": user,
        "stats": {
            "total_records": len(medical_records),
            "completed_records": completed_records,
            "pending_records": pending_records,
            "total_doctors": total_doctors
        },
        "recent_activities": recent_activities,
        "medical_records": medical_records,
        "family_history": family_history
    }
    
    return templates.TemplateResponse("dashboard.html", context)

# Add medical record
@app.post("/add_record")
async def add_record(
    request: Request,
    record_type: str = Form(...),
    record_date: str = Form(...),
    record_doctor: str = Form(...),
    record_notes: str = Form(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/signup")
    
    # Create new record
    new_record = {
        "id": len(medical_records_db[user["id"]]) + 1,
        "date": record_date,
        "type": record_type,
        "result": "Pending",
        "doctor": record_doctor,
        "notes": record_notes,
        "status": "pending",
        "status_color": "#f59e0b"
    }
    
    medical_records_db[user["id"]].append(new_record)
    
    return RedirectResponse(url="/dashboard", status_code=303)

# Update profile
@app.post("/update_profile")
async def update_profile(
    request: Request,
    full_name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    emergency_contact: str = Form(...),
    blood_type: str = Form(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/signup")
    
    # Update user data
    user["name"] = full_name
    user["age"] = age
    user["email"] = email
    user["phone"] = phone
    user["emergency_contact"] = emergency_contact
    user["blood_type"] = blood_type
    
    return RedirectResponse(url="/dashboard", status_code=303)

# Update medical info
@app.post("/update_medical_info")
async def update_medical_info(
    request: Request,
    allergies: str = Form(...),
    medications: str = Form(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/signup")
    
    # Update medical info
    user["allergies"] = allergies
    user["medications"] = medications
    
    return RedirectResponse(url="/dashboard", status_code=303)

# Add family member
@app.post("/add_family_member")
async def add_family_member(
    request: Request,
    relation: str = Form(...),
    age: int = Form(...),
    condition: str = Form(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/signup")
    
    # Add family member
    new_member = {
        "relation": relation,
        "age": age,
        "condition": condition
    }
    
    family_history_db[user["id"]].append(new_member)
    
    return RedirectResponse(url="/dashboard", status_code=303)

# Remove family member
@app.post("/remove_family_member")
async def remove_family_member(
    request: Request,
    index: int = Form(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/signup")
    
    # Remove family member
    if 0 <= index < len(family_history_db[user["id"]]):
        family_history_db[user["id"]].pop(index)
    
    return RedirectResponse(url="/dashboard", status_code=303)

# Logout
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response

# API endpoints for AJAX requests
@app.get("/api/stats")
async def get_stats(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    medical_records = medical_records_db.get(user["id"], [])
    completed_records = len([r for r in medical_records if r["status"] == "completed"])
    pending_records = len([r for r in medical_records if r["status"] == "pending"])
    total_doctors = len(set(r["doctor"] for r in medical_records))
    
    return {
        "total_records": len(medical_records),
        "completed_records": completed_records,
        "pending_records": pending_records,
        "total_doctors": total_doctors
    }
