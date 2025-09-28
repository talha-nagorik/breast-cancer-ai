from sqlmodel import SQLModel, create_engine, Session

# Database configuration
DATABASE_URL = "sqlite:///./app.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

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
