# FastAPI & Routing Documentation

This document provides comprehensive information about the FastAPI application structure, routing system, and API endpoints.

## 🏗️ Application Architecture

### Main Application (`app/main.py`)

The FastAPI application is initialized in `app/main.py` with the following configuration:

```python
app = FastAPI(
    title="AI Medical Records Application",
    description="A comprehensive medical records management system with AI-powered breast cancer detection",
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
```

### Key Features
- **Automatic API Documentation**: Available at `/docs` (Swagger UI) and `/redoc`
- **Static File Serving**: CSS, JS, and images served from `/static`
- **Template Rendering**: Jinja2 templates for HTML responses
- **GZip Compression**: Enabled for better performance
- **Database Initialization**: Automatic on startup

## 🛣️ Routing Structure

The application uses a modular routing system with separate routers for different functionalities:

### Router Organization

```
app/routers/
├── users.py         # User management and authentication
├── medical.py       # Medical records CRUD operations
├── ml.py           # Machine learning predictions
├── wisconsin.py    # Wisconsin dataset analysis
└── internal/
    └── admin.py    # Admin panel and internal operations
```

### Router Registration

```python
# Include all routers
app.include_router(users.router)
app.include_router(medical.router)
app.include_router(ml.router)
app.include_router(wisconsin.router)
app.include_router(admin.router)
```

## 📋 API Endpoints

### User Management (`/users`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/signup` | User registration page | No |
| POST | `/users/signup` | Create new user account | No |
| GET | `/users/login` | User login page | No |
| POST | `/users/login` | Authenticate user | No |
| POST | `/users/logout` | Logout user | Yes |
| GET | `/users/profile` | User profile page | Yes |
| POST | `/users/profile` | Update user profile | Yes |
| GET | `/users/dashboard` | User dashboard | Yes |

### Medical Records (`/medical`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/medical/records` | List medical records | Yes |
| POST | `/medical/records` | Add new medical record | Yes |
| GET | `/medical/records/{id}` | Get specific record | Yes |
| PUT | `/medical/records/{id}` | Update medical record | Yes |
| DELETE | `/medical/records/{id}` | Delete medical record | Yes |
| GET | `/medical/family-history` | Family history page | Yes |
| POST | `/medical/family-history` | Add family history | Yes |

### Machine Learning (`/ml`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/ml/api/train-model` | Train breast cancer model | Yes |
| POST | `/ml/api/predict` | Make breast cancer prediction | Yes |
| GET | `/ml/api/predictions` | Get user's prediction history | Yes |
| GET | `/ml/api/feature-importance` | Get feature importance | Yes |
| GET | `/ml/breast-cancer-analysis` | Analysis page | Yes |
| POST | `/ml/submit-prediction` | Submit prediction form | Yes |

### Wisconsin Dataset (`/wisconsin`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/wisconsin/api/dataset-info` | Dataset information | No |
| GET | `/wisconsin/api/feature-analysis` | Feature analysis | No |
| GET | `/wisconsin/api/feature-validation/{feature}` | Validate feature | No |
| POST | `/wisconsin/api/train-ensemble` | Train ensemble model | Yes |
| GET | `/wisconsin/api/ensemble-status` | Ensemble status | No |
| POST | `/wisconsin/api/predict` | Wisconsin prediction | Yes |
| GET | `/wisconsin/api/feature-importance` | Feature importance | Yes |
| GET | `/wisconsin/analytics` | Analytics dashboard | Yes |
| GET | `/wisconsin/prediction` | Prediction form | Yes |
| POST | `/wisconsin/prediction` | Submit prediction | Yes |

### Admin Panel (`/internal/admin`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/internal/admin` | Admin dashboard | Yes (Admin) |
| GET | `/internal/admin/users` | User management | Yes (Admin) |
| GET | `/internal/admin/analytics` | System analytics | Yes (Admin) |

## 🔐 Authentication System

### Session-Based Authentication

The application uses session-based authentication with the following components:

```python
# Session model
class Session(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime
    expires_at: datetime
    is_active: bool = Field(default=True)
```

### Authentication Flow

1. **Login**: User provides email/password
2. **Validation**: Credentials are verified
3. **Session Creation**: New session is created with expiration
4. **Cookie Setting**: Session ID is set as HTTP-only cookie
5. **Request Validation**: Each request validates session

### Dependency Injection

```python
async def get_current_user(session_id: str = Cookie(None)) -> User | None:
    """Get current user from session"""
    if not session_id:
        return None
    
    # Validate session and return user
    # Implementation in app/dependencies.py
```

## 📊 Request/Response Models

### Pydantic Models

The application uses Pydantic models for request/response validation:

```python
class PredictionRequest(BaseModel):
    features: dict[str, float]

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
    probabilities: dict[str, float]
```

### Response Types

- **HTML Responses**: For web pages using Jinja2 templates
- **JSON Responses**: For API endpoints
- **Redirect Responses**: For authentication flows

## 🎨 Template System

### Jinja2 Templates

Templates are located in the `templates/` directory:

```
templates/
├── base.html              # Base template
├── home.html              # Home page
├── login.html             # Login page
├── signup.html            # Registration page
├── dashboard.html         # User dashboard
├── breast_cancer_analysis.html
├── wisconsin_analytics.html
├── wisconsin_prediction.html
└── components/            # Reusable components
    ├── dashboard_nav.html
    ├── medical_records.html
    ├── family_history.html
    └── profile.html
```

### Template Context

Templates receive context data including:
- `request`: FastAPI request object
- `user`: Current authenticated user
- `error`: Error messages
- `success`: Success messages
- Component-specific data

## 🔧 Middleware and Configuration

### Middleware Stack

1. **GZip Middleware**: Compresses responses
2. **Static Files**: Serves static assets
3. **Template Engine**: Jinja2 for HTML rendering

### Configuration

```python
# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Middleware
app.add_middleware(GZipMiddleware)
```

## 🚀 Development vs Production

### Development Mode
```bash
uv run fastapi dev app/main.py
```
- Auto-reload on code changes
- Detailed error messages
- Debug mode enabled

### Production Mode
```bash
uv run fastapi run app/main.py
```
- Optimized performance
- Error logging
- Production-ready configuration

## 📝 API Documentation

### Automatic Documentation

FastAPI automatically generates:
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`

### Custom Documentation

Each endpoint includes:
- Summary and description
- Request/response models
- Authentication requirements
- Example requests/responses

## 🧪 Testing API Endpoints

### Using curl

```bash
# Test health endpoint
curl http://localhost:8000/

# Test API documentation
curl http://localhost:8000/docs

# Test prediction (requires authentication)
curl -X POST "http://localhost:8000/ml/api/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": {...}}' \
  -b "session_id=your_session_id"
```

### Using Python requests

```python
import requests

# Test prediction
response = requests.post(
    "http://localhost:8000/ml/api/predict",
    json={"features": {...}},
    cookies={"session_id": "your_session_id"}
)
print(response.json())
```

## 🔍 Error Handling

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

### Error Responses

```python
# Example error response
{
    "detail": "Error message",
    "status_code": 400
}
```

## 📈 Performance Considerations

### Optimization Features

1. **GZip Compression**: Reduces response size
2. **Static File Caching**: Efficient asset serving
3. **Database Connection Pooling**: Optimized DB access
4. **Async/Await**: Non-blocking request handling

### Monitoring

- Request/response logging
- Performance metrics
- Error tracking
- Database query optimization

## 🔧 Customization

### Adding New Routes

1. Create new router file in `app/routers/`
2. Define endpoints with proper decorators
3. Include router in `app/main.py`
4. Add authentication if required

### Adding Middleware

```python
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # Custom middleware logic
    response = await call_next(request)
    return response
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

---

For more information about specific components, see:
- [Database Documentation](DATABASE.md)
- [AI/ML Documentation](AI_ML.md)
- [Web Frontend Documentation](WEB_FRONTEND.md)
