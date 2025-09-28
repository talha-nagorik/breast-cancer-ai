#!/usr/bin/env python3
"""
Database management CLI script.

This script provides easy access to database management commands.
"""

from app.database.init import (
    initialize_database,
    check_migration_status,
    apply_migrations,
    create_migration,
    downgrade_database,
    show_migration_history
)
import sys
from pathlib import Path
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_header(text: str) -> None:
    """Print a colored header."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{text.center(60)}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")


def print_success(text: str) -> None:
    """Print success message in green."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_error(text: str) -> None:
    """Print error message in red."""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_warning(text: str) -> None:
    """Print warning message in yellow."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_info(text: str) -> None:
    """Print info message in blue."""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")


def print_command_help() -> None:
    """Print colored command help."""
    print(f"{Fore.CYAN}{Style.BRIGHT}Database Management CLI{Style.RESET_ALL}")
    print(
        f"{Fore.WHITE}Usage: {Style.BRIGHT}python manage_db.py <command> [options]{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Available Commands:{Style.RESET_ALL}")
    commands = [
        ("init", "Initialize database and apply migrations", Fore.GREEN),
        ("status", "Show migration status", Fore.BLUE),
        ("migrate", "Apply pending migrations", Fore.CYAN),
        ("create-migration", "Create a new migration", Fore.MAGENTA),
        ("downgrade [revision]",
         "Downgrade database (default: -1)", Fore.YELLOW),
        ("history", "Show migration history", Fore.WHITE)
    ]

    for cmd, desc, color in commands:
        print(f"  {color}{Style.BRIGHT}{cmd:<20}{Style.RESET_ALL} - {desc}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Examples:{Style.RESET_ALL}")
    examples = [
        "python manage_db.py init",
        "python manage_db.py status",
        "python manage_db.py create-migration 'Add new table'",
        "python manage_db.py downgrade",
        "python manage_db.py downgrade base"
    ]

    for example in examples:
        print(f"  {Fore.CYAN}{example}{Style.RESET_ALL}")


def print_status_table(status: dict) -> None:
    """Print migration status in a nice table format."""
    print_header("Migration Status")

    # Define status colors and icons
    status_config = {
        "database_exists": (Fore.GREEN if status["database_exists"] else Fore.RED, "✓" if status["database_exists"] else "✗"),
        "current_revision": (Fore.CYAN, "📋"),
        "head_revision": (Fore.BLUE, "🎯"),
        "is_up_to_date": (Fore.GREEN if status["is_up_to_date"] else Fore.YELLOW, "✓" if status["is_up_to_date"] else "⚠"),
        "pending_migrations": (Fore.RED if status["pending_migrations"] else Fore.GREEN, "⚠" if status["pending_migrations"] else "✓")
    }

    for key, value in status.items():
        color, icon = status_config.get(key, (Fore.WHITE, "•"))
        display_name = key.replace('_', ' ').title()
        print(f"{color}{icon} {display_name:<20}{Style.RESET_ALL}: {value}")


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print_command_help()
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "init":
            print_header("Database Initialization")
            print_info("Starting database initialization...")
            initialize_database()
            print_success("Database initialization completed successfully!")

        elif command == "status":
            status = check_migration_status()
            print_status_table(status)

        elif command == "migrate":
            print_header("Applying Migrations")
            print_info("Checking for pending migrations...")
            apply_migrations()
            print_success("All migrations applied successfully!")

        elif command == "create-migration":
            if len(sys.argv) < 3:
                print_error("Migration message is required")
                print_info(
                    "Usage: python manage_db.py create-migration 'Your message here'")
                sys.exit(1)
            message = sys.argv[2]
            print_header("Creating Migration")
            print_info(f"Creating migration: {message}")
            create_migration(message)
            print_success(f"Migration '{message}' created successfully!")

        elif command == "downgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
            print_header("Database Downgrade")
            print_warning(f"Downgrading database to revision: {revision}")
            downgrade_database(revision)
            print_success("Database downgrade completed!")

        elif command == "history":
            print_header("Migration History")
            show_migration_history()

        else:
            print_error(f"Unknown command: {command}")
            print_info(
                "Use 'python manage_db.py' without arguments to see available commands.")
            sys.exit(1)

    except Exception as e:
        print_error(f"Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
