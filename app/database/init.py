"""
Database initialization and migration management module.

This module handles:
1. Database file creation if it doesn't exist
2. Alembic migration tracking and application
3. Proper startup sequence for the application
"""

import sys

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from .database import DATABASE_URL, engine


def get_alembic_config() -> Config:
    """Get Alembic configuration."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    alembic_cfg = Config(str(project_root / "alembic.ini"))

    # Set the database URL in the config
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    return alembic_cfg


def database_exists() -> bool:
    """Check if the database file exists."""
    db_path = Path("app.db")
    return db_path.exists()


def create_database() -> None:
    """Create the database file and initialize it."""
    print("Creating database...")

    # Create the database file by connecting to it
    # SQLite will create the file if it doesn't exist
    test_engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30,
        },
        pool_pre_ping=True,
    )
    with test_engine.connect() as conn:
        # Execute a simple query to ensure the database is created
        conn.execute(text("SELECT 1"))

    print("Database created successfully.")


def get_current_revision() -> str | None:
    """Get the current database revision."""
    try:
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            return context.get_current_revision()
    except OperationalError:
        # Database doesn't exist or alembic_version table doesn't exist
        return None


def get_head_revision() -> str:
    """Get the head revision from the migration scripts."""
    alembic_cfg = get_alembic_config()
    script_dir = ScriptDirectory.from_config(alembic_cfg)
    return script_dir.get_current_head()


def apply_migrations() -> None:
    """Apply pending migrations to the database."""
    current_rev = get_current_revision()
    head_rev = get_head_revision()

    if current_rev != head_rev:
        print(f"Applying migrations from {current_rev} to {head_rev}...")
        alembic_cfg = get_alembic_config()
        command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully.")
    else:
        print("Database is up to date.")


def initialize_database() -> None:
    """
    Initialize the database with proper migration handling.

    This function:
    1. Creates the database if it doesn't exist
    2. Applies any pending migrations
    3. Ensures the database is ready for the application
    """
    print("Initializing database...")

    # Step 1: Create database if it doesn't exist
    if not database_exists():
        create_database()

    # Step 2: Apply migrations
    apply_migrations()

    print("Database initialization completed.")


def check_migration_status() -> dict:
    """
    Check the current migration status.

    Returns:
        dict: Status information including current revision, head revision, and pending migrations
    """
    current_rev = get_current_revision()
    head_rev = get_head_revision()

    status = {
        "database_exists": database_exists(),
        "current_revision": current_rev,
        "head_revision": head_rev,
        "is_up_to_date": current_rev == head_rev,
        "pending_migrations": current_rev != head_rev
    }

    return status


def create_migration(message: str) -> None:
    """
    Create a new migration file.

    Args:
        message: Description of the migration
    """
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, autogenerate=True, message=message)
    print(f"Migration created: {message}")


def downgrade_database(revision: str = "-1") -> None:
    """
    Downgrade the database to a specific revision.

    Args:
        revision: Target revision (default: -1 for one step back)
    """
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)
    print(f"Database downgraded to revision: {revision}")


def show_migration_history() -> None:
    """Show the migration history."""
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)


if __name__ == "__main__":
    # CLI interface for database management
    import argparse

    parser = argparse.ArgumentParser(description="Database management CLI")
    parser.add_argument("command", choices=[
        "init", "status", "migrate", "create-migration",
        "downgrade", "history"
    ], help="Command to execute")
    parser.add_argument(
        "--message", help="Migration message (for create-migration)")
    parser.add_argument("--revision", help="Target revision (for downgrade)")

    args = parser.parse_args()

    if args.command == "init":
        initialize_database()
    elif args.command == "status":
        status = check_migration_status()
        print("Migration Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    elif args.command == "migrate":
        apply_migrations()
    elif args.command == "create-migration":
        if not args.message:
            print("Error: --message is required for create-migration")
            sys.exit(1)
        create_migration(args.message)
    elif args.command == "downgrade":
        revision = args.revision or "-1"
        downgrade_database(revision)
    elif args.command == "history":
        show_migration_history()
