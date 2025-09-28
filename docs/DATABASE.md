# Database & Migrations Documentation

This document provides comprehensive information about the database system, models, migrations, and the database management CLI.

## 🗄️ Database Architecture

### Database Engine
- **Primary**: SQLite (development and production)
- **Alternative**: PostgreSQL/MySQL (configurable)
- **ORM**: SQLModel (built on SQLAlchemy)
- **Migrations**: Alembic

### Database Configuration

The database configuration is located in `app/database/database.py`:

```python
# Default SQLite configuration
DATABASE_URL = "sqlite:///./app.db"

# For PostgreSQL
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

# For MySQL
# DATABASE_URL = "mysql://user:password@localhost/dbname"
```

## 📊 Database Models

### User Model

```python
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)  # UUID
    name: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    password_hash: str
    age: Optional[int] = Field(default=0)
    phone: Optional[str] = Field(default="")
    emergency_contact: Optional[str] = Field(default="")
    blood_type: Optional[str] = Field(default="O+")
    allergies: Optional[str] = Field(default="")
    medications: Optional[str] = Field(default="")
    created_at: datetime
    updated_at: datetime
    is_active: bool = Field(default=True)
```

**Key Features:**
- UUID primary key for security
- Email uniqueness and indexing
- Medical information fields
- Timestamps for audit trail
- Soft delete capability

### MedicalRecord Model

```python
class MedicalRecord(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    date: str = Field(max_length=20)
    type: str = Field(max_length=100)
    result: str = Field(max_length=100)
    doctor: str = Field(max_length=100)
    notes: str = Field(max_length=1000)
    status: str = Field(default="pending")
    status_color: str = Field(default="#f59e0b")
    created_at: datetime
```

**Key Features:**
- Foreign key relationship to User
- Status tracking with color coding
- Comprehensive medical information
- Audit timestamps

### FamilyHistory Model

```python
class FamilyHistory(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    relation: str = Field(max_length=50)
    age: int
    condition: str = Field(max_length=200)
    created_at: datetime
```

**Key Features:**
- Family relationship tracking
- Age and condition information
- User association

### Session Model

```python
class Session(SQLModel, table=True):
    id: str = Field(primary_key=True)  # UUID
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime
    expires_at: datetime
    is_active: bool = Field(default=True)
```

**Key Features:**
- Session management
- Automatic expiration
- User association

### BreastCancerPrediction Model

```python
class BreastCancerPrediction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    
    # 30 Wisconsin dataset features
    radius_mean: float
    texture_mean: float
    # ... (all 30 features)
    
    # Prediction results
    prediction: str  # "Benign" or "Malignant"
    confidence: float
    risk_level: str  # "Low", "Medium", "High"
    
    created_at: datetime
    notes: Optional[str] = Field(default="")
```

**Key Features:**
- Complete Wisconsin dataset feature storage
- Prediction results with confidence
- Risk level assessment
- User association

## 🔄 Migration System

### Alembic Configuration

The migration system uses Alembic with configuration in `alembic.ini`:

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = sqlite:///./app.db

[post_write_hooks]
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 79 REVISION_SCRIPT_FILENAME
```

### Migration Files

Migrations are stored in `alembic/versions/`:

```
alembic/versions/
├── a8b9ec836410_initial_migration.py
└── d24a4742aa81_add_breast_cancer_prediction_model.py
```

### Migration Lifecycle

1. **Create Migration**: `uv run python manage_db.py create-migration "Description"`
2. **Review Migration**: Check generated SQL in version file
3. **Apply Migration**: `uv run python manage_db.py migrate`
4. **Verify**: `uv run python manage_db.py status`

## 🛠️ Database Management CLI

The `manage_db.py` script provides a comprehensive CLI for database operations:

### Available Commands

#### Initialize Database
```bash
uv run python manage_db.py init
```
- Creates database file if it doesn't exist
- Applies all pending migrations
- Sets up initial schema

#### Check Status
```bash
uv run python manage_db.py status
```
Shows:
- Database existence
- Current revision
- Head revision
- Pending migrations
- Migration status

#### Apply Migrations
```bash
uv run python manage_db.py migrate
```
- Applies all pending migrations
- Updates database schema
- Safe operation (can be run multiple times)

#### Create Migration
```bash
uv run python manage_db.py create-migration "Add new table"
```
- Generates new migration file
- Auto-detects model changes
- Requires manual review before applying

#### Migration History
```bash
uv run python manage_db.py history
```
- Shows all migrations
- Displays revision chain
- Shows applied status

#### Downgrade Database
```bash
# Downgrade one step
uv run python manage_db.py downgrade

# Downgrade to specific revision
uv run python manage_db.py downgrade a8b9ec836410

# Downgrade to base (remove all tables)
uv run python manage_db.py downgrade base
```

### CLI Features

- **Colored Output**: Easy-to-read status information
- **Error Handling**: Comprehensive error messages
- **Safety Checks**: Prevents destructive operations
- **Status Validation**: Verifies migration state

## 🔧 Database Operations

### Connection Management

```python
# Database engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection
def get_session():
    with SessionLocal() as session:
        yield session
```

### Query Examples

#### User Operations
```python
# Create user
user = User(name="John Doe", email="john@example.com", ...)
session.add(user)
session.commit()

# Get user by email
user = session.exec(select(User).where(User.email == "john@example.com")).first()

# Update user
user.name = "John Smith"
session.commit()
```

#### Medical Records
```python
# Get user's medical records
records = session.exec(
    select(MedicalRecord)
    .where(MedicalRecord.user_id == user.id)
    .order_by(MedicalRecord.created_at.desc())
).all()

# Add new record
record = MedicalRecord(
    user_id=user.id,
    date="2024-01-15",
    type="Blood Test",
    result="Normal",
    doctor="Dr. Smith"
)
session.add(record)
session.commit()
```

#### Predictions
```python
# Get user's predictions
predictions = session.exec(
    select(BreastCancerPrediction)
    .where(BreastCancerPrediction.user_id == user.id)
    .order_by(BreastCancerPrediction.created_at.desc())
).all()

# Save prediction
prediction = BreastCancerPrediction(
    user_id=user.id,
    radius_mean=12.5,
    texture_mean=18.2,
    # ... all features
    prediction="Benign",
    confidence=0.95,
    risk_level="Low"
)
session.add(prediction)
session.commit()
```

## 🔒 Security Considerations

### Data Protection
- **Password Hashing**: Uses pbkdf2_sha256
- **SQL Injection**: Prevented by SQLModel/SQLAlchemy
- **Session Security**: UUID-based session IDs
- **Data Validation**: Pydantic model validation

### Access Control
- **User Isolation**: Users can only access their own data
- **Session Validation**: Automatic session expiration
- **Admin Controls**: Separate admin routes

## 📊 Database Performance

### Indexing Strategy
- **Primary Keys**: Automatic indexing
- **Foreign Keys**: Automatic indexing
- **Email Field**: Unique index for fast lookups
- **Timestamps**: Consider adding indexes for large datasets

### Query Optimization
- **Lazy Loading**: Default SQLAlchemy behavior
- **Eager Loading**: Use `selectinload()` for related data
- **Connection Pooling**: Automatic with SQLAlchemy
- **Query Caching**: Consider Redis for production

## 🚀 Production Considerations

### Database Scaling
- **SQLite Limitations**: Single writer, file-based
- **PostgreSQL**: Recommended for production
- **Connection Pooling**: Configure for high concurrency
- **Read Replicas**: For read-heavy workloads

### Backup Strategy
```bash
# SQLite backup
cp app.db app.db.backup

# PostgreSQL backup
pg_dump database_name > backup.sql

# Automated backups
# Consider implementing scheduled backups
```

### Monitoring
- **Query Performance**: Monitor slow queries
- **Connection Usage**: Track connection pool
- **Migration Status**: Regular status checks
- **Data Integrity**: Periodic validation

## 🧪 Testing Database

### Test Database Setup
```python
# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

# Or separate test database
TEST_DATABASE_URL = "sqlite:///./test_app.db"
```

### Database Testing
```bash
# Test database connection
uv run python -c "from app.database import engine; print('✅ Database connection successful')"

# Test migrations
uv run python manage_db.py status

# Test model imports
uv run python -c "from app.models.models import User; print('✅ Models import successfully')"
```

## 🔧 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   # Check migration status
   uv run python manage_db.py status
   
   # Reset to last working migration
   uv run python manage_db.py downgrade
   ```

2. **Database Locked**
   ```bash
   # Check for running processes
   lsof app.db  # macOS/Linux
   
   # Restart application
   ```

3. **Schema Mismatch**
   ```bash
   # Recreate database
   rm app.db
   uv run python manage_db.py init
   ```

4. **Foreign Key Errors**
   - Check data integrity
   - Verify user IDs exist
   - Review migration order

### Recovery Procedures

1. **Backup First**: Always backup before major changes
2. **Test Migrations**: Test on copy of production data
3. **Rollback Plan**: Know how to downgrade
4. **Data Validation**: Verify data integrity after migrations

## 📚 Additional Resources

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

For more information about other components, see:
- [FastAPI Documentation](FASTAPI.md)
- [AI/ML Documentation](AI_ML.md)
- [Web Frontend Documentation](WEB_FRONTEND.md)
