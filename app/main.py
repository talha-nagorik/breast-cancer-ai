"""
AI Medical Records Application - Main FastAPI Application

This module contains the main FastAPI application setup, configuration,
and core routes for the AI Medical Records system.

Features:
- User management and authentication
- Medical records tracking
- Family history management
- AI-powered breast cancer detection
- Wisconsin dataset analysis

Author: AI Medical Records Team
Version: 1.0.0
"""

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware

from .database.init import initialize_database
from .routers import users, medical, ml, wisconsin
from .internal import admin
from .dependencies import get_current_user
from .models.models import User

# Initialize FastAPI application with comprehensive configuration
app = FastAPI(
    title="AI Medical Records Application",
    description="""
    A comprehensive medical records management system with AI-powered breast cancer detection.
    
    ## Features
    
    * **User Management**: Secure registration, login, and session management
    * **Medical Records**: Track medical history, test results, and doctor information
    * **Family History**: Manage family medical history and genetic information
    * **AI Breast Cancer Detection**: Advanced machine learning models for breast cancer prediction
    * **Wisconsin Dataset Analysis**: Specialized analysis using the Wisconsin Breast Cancer Dataset
    
    ## AI Models
    
    * **Standard Model**: Random Forest classifier with 97%+ accuracy
    * **Wisconsin Ensemble**: 8-model ensemble with 98.25% accuracy and 99.97% ROC AUC
    
    ## Authentication
    
    Most endpoints require user authentication. Use the `/users/signup` and `/users/login` endpoints to create an account.
    """,
    version="1.0.0",
    contact={
        "name": "AI Medical Records Team",
        "email": "support@aimedicalrecords.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add GZip compression middleware for better performance
app.add_middleware(GZipMiddleware)

# Setup Jinja2 templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Include all API routers
app.include_router(users.router)        # User management and authentication
app.include_router(medical.router)      # Medical records and family history
app.include_router(ml.router)          # Machine learning predictions
app.include_router(wisconsin.router)   # Wisconsin dataset analysis
app.include_router(admin.router)       # Admin panel and internal operations


@app.on_event("startup")
async def on_startup() -> None:
    """
    Application startup event handler.

    Initializes the database and applies any pending migrations
    when the application starts up.

    This ensures the database is ready before handling any requests.
    """
    initialize_database()

# Home page


@app.get("/",
         response_class=HTMLResponse,
         tags=["Application"],
         summary="Home Page",
         description="Welcome page with application overview and features")
async def home(request: Request, user: User | None = Depends(get_current_user)) -> HTMLResponse:
    """
    Home page endpoint.

    Displays the welcome page with application overview, features,
    and information about AI breast cancer detection capabilities.

    Args:
        request: FastAPI request object
        user: Current authenticated user (optional)

    Returns:
        HTMLResponse: Rendered home page template

    Features displayed:
        - Application statistics
        - About cards with key information
        - Breast cancer symptoms
        - Detection process steps
        - Risk factors information
    """
    # Prepare context data for the home page template
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
                "description": "Using cutting-edge artificial intelligence and machine learning algorithms, our system provides accurate, non-invasive breast cancer detection using the Wisconsin dataset."
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
            {"number": 1, "title": "Input Features",
                "description": "Enter your medical test results and measurements"},
            {"number": 2, "title": "AI Analysis",
                "description": "Our AI algorithms analyze the data using the Wisconsin dataset"},
            {"number": 3, "title": "Risk Assessment",
                "description": "Get detailed risk assessment and confidence scores"},
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
