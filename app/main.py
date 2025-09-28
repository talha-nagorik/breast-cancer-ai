from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from typing import Optional

from .database.database import create_db_and_tables
from .dependencies import get_current_user
from .routers import users, medical
from .internal import admin

app = FastAPI(title="AI Medical Records Application")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(users.router)
app.include_router(medical.router)
app.include_router(admin.router)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user: Optional[dict] = None):
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
            {"icon": "🔴", "title": "Lump or Mass",
                "description": "A new lump or mass in the breast or underarm area"},
            {"icon": "🔄", "title": "Shape Changes",
                "description": "Changes in breast size, shape, or appearance"},
            {"icon": "💧", "title": "Nipple Discharge",
                "description": "Clear or bloody discharge from the nipple"},
            {"icon": "🔴", "title": "Skin Changes",
                "description": "Redness, dimpling, or puckering of breast skin"},
            {"icon": "😣", "title": "Pain",
                "description": "Breast pain or tenderness that doesn't go away"},
            {"icon": "🔄", "title": "Nipple Changes",
                "description": "Nipple turning inward or changing position"}
        ],
        "detection_steps": [
            {"number": 1, "title": "Upload Images",
                "description": "Upload your mammogram or ultrasound images securely"},
            {"number": 2, "title": "AI Analysis",
                "description": "Our AI algorithms analyze the images for abnormalities"},
            {"number": 3, "title": "Expert Review",
                "description": "Results are reviewed by certified radiologists"},
            {"number": 4, "title": "Detailed Report",
                "description": "Receive comprehensive results and recommendations"}
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
