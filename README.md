# AI Medical Records Application

A comprehensive medical records management system with user authentication, built with FastAPI, SQLModel, and SQLite.

## 🏗️ Project Structure

```
ai/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── main.py              # Main FastAPI app
│   ├── dependencies.py      # Dependency injection
│   ├── models.py            # Database models
│   ├── database.py          # Database configuration
│   ├── auth.py              # Authentication utilities
│   ├── routers/             # API routes
│   │   ├── __init__.py
│   │   ├── users.py         # User management routes
│   │   └── items.py         # Medical records routes
│   └── internal/            # Internal/admin routes
│       ├── __init__.py
│       └── admin.py         # Admin panel
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   ├── env.py              # Alembic environment configuration
│   └── script.py.mako      # Migration template
├── templates/              # Jinja2 HTML templates
├── static/                 # Static files (CSS, JS, images)
├── main.py                 # Application entry point
├── alembic.ini            # Alembic configuration
├── pyproject.toml         # Project dependencies and configuration
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Run Database Migrations

```bash
uv run alembic upgrade head
```

### 3. Start the Application

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application

Visit: http://localhost:8000

## 🎯 Features

### User Management
- ✅ User registration with email validation
- ✅ Secure login with password hashing
- ✅ Session-based authentication
- ✅ User profile management

### Medical Records
- ✅ Add/edit medical records
- ✅ Track record status (pending/completed)
- ✅ Doctor information and notes
- ✅ Date-based organization

### Family History
- ✅ Add family members
- ✅ Track medical conditions
- ✅ Age and relationship tracking

### Security
- ✅ Password hashing with pbkdf2_sha256
- ✅ Session management with expiration
- ✅ SQL injection protection via SQLModel
- ✅ Secure cookie handling

## 🗄️ Database Models

### User
- Personal information (name, email, age, phone)
- Medical information (blood type, allergies, medications)
- Emergency contact information
- Account status and timestamps

### MedicalRecord
- Record type and date
- Doctor information and notes
- Result and status tracking
- User association

### FamilyHistory
- Family relationship
- Age and medical conditions
- User association

### Session
- User session management
- Expiration tracking
- Active status

## 🔧 Development

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
uv run alembic upgrade head

# Check current migration status
uv run alembic current

# View migration history
uv run alembic history
```

### Testing

```bash
# Test application imports
uv run python -c "from app.main import app; print('✅ App imports successfully')"

# Test database connection
uv run python -c "from app.database import engine; print('✅ Database connection successful')"
```

## 📦 Package Structure Benefits

### Why This Layout?

1. **Clean Separation**: Application code is organized in logical modules
2. **Import Clarity**: Clear import paths (`from app.models import User`)
3. **Testing**: Easier to test individual components
4. **Deployment**: Better for packaging and distribution
5. **IDE Support**: Better autocomplete and navigation
6. **Scalability**: Easy to add new modules and features
7. **FastAPI Best Practices**: Follows standard FastAPI project structure

### Module Organization

- **`app/main.py`**: FastAPI application and main routes
- **`app/models.py`**: Database models and schemas
- **`app/database.py`**: Database configuration and session management
- **`app/auth.py`**: Authentication and security utilities
- **`app/dependencies.py`**: Dependency injection functions
- **`app/routers/`**: API route modules (users, items)
- **`app/internal/`**: Internal/admin routes

## 🔒 Security Features

- **Password Hashing**: Uses pbkdf2_sha256 for secure password storage
- **Session Management**: Database-backed sessions with expiration
- **Input Validation**: FastAPI automatic request validation
- **SQL Injection Protection**: SQLModel provides built-in protection
- **CSRF Protection**: Session-based authentication

## 🎨 Frontend

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Interactive Forms**: Real-time validation and feedback
- **Dashboard**: Comprehensive overview of medical records
- **Mobile Friendly**: Responsive design for all devices

## 📝 Sample User

For testing purposes, a sample user is available:
- **Email**: jane.doe@email.com
- **Password**: password123

## 🛠️ Configuration

### Environment Variables

- `SECRET_KEY`: JWT secret key (defaults to development key)
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### Database

The application uses SQLite by default, but can be easily configured for PostgreSQL or MySQL by updating the `DATABASE_URL` in `src/ai/database/database.py`.

## 📈 Future Enhancements

- [ ] Image upload for medical records
- [ ] Email notifications
- [ ] API documentation with Swagger
- [ ] User roles and permissions
- [ ] Data export functionality
- [ ] Advanced search and filtering
- [ ] Mobile app integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
