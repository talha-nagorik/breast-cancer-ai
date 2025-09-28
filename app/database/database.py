from sqlmodel import SQLModel, create_engine, Session

# Database configuration
DATABASE_URL = "sqlite:///./app.db"

# Create engine with SQLite-specific configurations
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={
        "check_same_thread": False,  # Allow multiple threads to access the database
        "timeout": 30,  # Wait up to 30 seconds for database lock
    },
    pool_pre_ping=True,  # Verify connections before use
)

# Note: Database initialization is now handled by app.database.init module
# This function is kept for backward compatibility but should not be used


def create_db_and_tables():
    """Create database tables - DEPRECATED: Use initialize_database() instead"""
    import warnings
    warnings.warn(
        "create_db_and_tables() is deprecated. Use initialize_database() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
