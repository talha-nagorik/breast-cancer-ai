"""
Database Models for AI Medical Records Application

This module defines all database models using SQLModel (built on SQLAlchemy).
The models represent the core entities in the medical records system.

Models:
- User: User account and profile information
- MedicalRecord: Medical test results and records
- FamilyHistory: Family medical history tracking
- Session: User session management
- BreastCancerPrediction: AI prediction results and features

Author: AI Medical Records Team
Version: 1.0.0
"""

import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class User(SQLModel, table=True):
    """
    User model representing a user account in the medical records system.

    This model stores user profile information, medical details, and account status.
    Uses UUID as primary key for security and uniqueness.

    Attributes:
        id: Unique identifier (UUID string)
        name: User's full name
        email: User's email address (unique, indexed)
        password_hash: Hashed password for authentication
        age: User's age
        phone: Contact phone number
        emergency_contact: Emergency contact information
        blood_type: User's blood type
        allergies: Known allergies and reactions
        medications: Current medications
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        is_active: Account status flag
    """
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique user identifier (UUID)"
    )
    name: str = Field(
        max_length=100,
        description="User's full name"
    )
    email: str = Field(
        max_length=100,
        unique=True,
        index=True,
        description="User's email address (unique)"
    )
    password_hash: str = Field(
        max_length=255,
        description="Hashed password for secure authentication"
    )
    age: Optional[int] = Field(
        default=0,
        description="User's age"
    )
    phone: Optional[str] = Field(
        default="",
        max_length=20,
        description="Contact phone number"
    )
    emergency_contact: Optional[str] = Field(
        default="",
        max_length=100,
        description="Emergency contact information"
    )
    blood_type: Optional[str] = Field(
        default="O+",
        max_length=5,
        description="User's blood type"
    )
    allergies: Optional[str] = Field(
        default="",
        max_length=500,
        description="Known allergies and reactions"
    )
    medications: Optional[str] = Field(
        default="",
        max_length=500,
        description="Current medications"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update timestamp"
    )
    is_active: bool = Field(
        default=True,
        description="Account active status"
    )


class MedicalRecord(SQLModel, table=True):
    """
    Medical record model for storing medical test results and records.

    This model tracks medical tests, results, doctor information, and status.
    Each record is associated with a specific user.

    Attributes:
        id: Unique record identifier
        user_id: Foreign key reference to User
        date: Date of the medical test/record
        type: Type of medical test or record
        result: Test result or outcome
        doctor: Doctor or healthcare provider name
        notes: Additional notes or comments
        status: Record status (pending, completed, etc.)
        status_color: Color code for status display
        created_at: Record creation timestamp
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique medical record identifier"
    )
    user_id: str = Field(
        foreign_key="user.id",
        description="Reference to the user who owns this record"
    )
    date: str = Field(
        max_length=20,
        description="Date of the medical test or record"
    )
    type: str = Field(
        max_length=100,
        description="Type of medical test or record"
    )
    result: str = Field(
        max_length=100,
        description="Test result or outcome"
    )
    doctor: str = Field(
        max_length=100,
        description="Doctor or healthcare provider name"
    )
    notes: str = Field(
        max_length=1000,
        description="Additional notes or comments"
    )
    status: str = Field(
        max_length=20,
        default="pending",
        description="Record status (pending, completed, etc.)"
    )
    status_color: str = Field(
        max_length=10,
        default="#f59e0b",
        description="Color code for status display in UI"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Record creation timestamp"
    )


class FamilyHistory(SQLModel, table=True):
    """
    Family history model for tracking family medical conditions.

    This model stores information about family members and their medical conditions
    to help assess genetic risk factors.

    Attributes:
        id: Unique record identifier
        user_id: Foreign key reference to User
        relation: Family relationship (mother, father, sister, etc.)
        age: Age of the family member
        condition: Medical condition or diagnosis
        created_at: Record creation timestamp
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique family history record identifier"
    )
    user_id: str = Field(
        foreign_key="user.id",
        description="Reference to the user who owns this family history"
    )
    relation: str = Field(
        max_length=50,
        description="Family relationship (mother, father, sister, etc.)"
    )
    age: int = Field(
        description="Age of the family member"
    )
    condition: str = Field(
        max_length=200,
        description="Medical condition or diagnosis"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Record creation timestamp"
    )


class Session(SQLModel, table=True):
    """
    Session model for managing user authentication sessions.

    This model tracks active user sessions with expiration times
    for secure session management.

    Attributes:
        id: Unique session identifier (UUID)
        user_id: Foreign key reference to User
        created_at: Session creation timestamp
        expires_at: Session expiration timestamp
        is_active: Session active status
    """
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique session identifier (UUID)"
    )
    user_id: str = Field(
        foreign_key="user.id",
        description="Reference to the user who owns this session"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Session creation timestamp"
    )
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc).replace(hour=23, minute=59, second=59),
        description="Session expiration timestamp"
    )
    is_active: bool = Field(
        default=True,
        description="Session active status"
    )


class BreastCancerPrediction(SQLModel, table=True):
    """
    Breast cancer prediction model for storing AI prediction results.

    This model stores the complete Wisconsin dataset features used for prediction
    along with the AI model's prediction results, confidence scores, and risk assessment.

    The model includes all 30 features from the Wisconsin Breast Cancer Dataset:
    - 10 mean features (radius_mean, texture_mean, etc.)
    - 10 standard error features (radius_se, texture_se, etc.)
    - 10 worst features (radius_worst, texture_worst, etc.)

    Attributes:
        id: Unique prediction record identifier
        user_id: Foreign key reference to User

        # Wisconsin Dataset Features (30 total)
        radius_mean: Mean distance from center to points on perimeter
        texture_mean: Standard deviation of gray-scale values
        perimeter_mean: Mean perimeter of the nucleus
        area_mean: Mean area of the nucleus
        smoothness_mean: Mean local variation in radius lengths
        compactness_mean: Mean (perimeter² / area - 1.0)
        concavity_mean: Mean severity of concave portions of the contour
        concave_points_mean: Mean number of concave portions of the contour
        symmetry_mean: Mean symmetry of the nucleus
        fractal_dimension_mean: Mean "coastline approximation" - 1

        # Standard Error Features (se)
        radius_se, texture_se, perimeter_se, area_se, smoothness_se,
        compactness_se, concavity_se, concave_points_se, symmetry_se,
        fractal_dimension_se: Standard error of corresponding mean features

        # Worst Features
        radius_worst, texture_worst, perimeter_worst, area_worst,
        smoothness_worst, compactness_worst, concavity_worst,
        concave_points_worst, symmetry_worst, fractal_dimension_worst:
        Worst (largest) values of corresponding features

        # Prediction Results
        prediction: AI prediction result ("Benign" or "Malignant")
        confidence: Confidence score (0.0 to 1.0)
        risk_level: Risk assessment ("Low", "Medium", "High")

        # Metadata
        created_at: Prediction timestamp
        notes: Additional notes or comments
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique prediction record identifier"
    )
    user_id: str = Field(
        foreign_key="user.id",
        description="Reference to the user who owns this prediction"
    )

    # Wisconsin Dataset Features - Mean (10 features)
    radius_mean: float = Field(
        description="Mean distance from center to points on perimeter")
    texture_mean: float = Field(
        description="Standard deviation of gray-scale values")
    perimeter_mean: float = Field(description="Mean perimeter of the nucleus")
    area_mean: float = Field(description="Mean area of the nucleus")
    smoothness_mean: float = Field(
        description="Mean local variation in radius lengths")
    compactness_mean: float = Field(
        description="Mean (perimeter² / area - 1.0)")
    concavity_mean: float = Field(
        description="Mean severity of concave portions of the contour")
    concave_points_mean: float = Field(
        description="Mean number of concave portions of the contour")
    symmetry_mean: float = Field(description="Mean symmetry of the nucleus")
    fractal_dimension_mean: float = Field(
        description="Mean 'coastline approximation' - 1")

    # Wisconsin Dataset Features - Standard Error (10 features)
    radius_se: float = Field(description="Standard error of radius_mean")
    texture_se: float = Field(description="Standard error of texture_mean")
    perimeter_se: float = Field(description="Standard error of perimeter_mean")
    area_se: float = Field(description="Standard error of area_mean")
    smoothness_se: float = Field(
        description="Standard error of smoothness_mean")
    compactness_se: float = Field(
        description="Standard error of compactness_mean")
    concavity_se: float = Field(description="Standard error of concavity_mean")
    concave_points_se: float = Field(
        description="Standard error of concave_points_mean")
    symmetry_se: float = Field(description="Standard error of symmetry_mean")
    fractal_dimension_se: float = Field(
        description="Standard error of fractal_dimension_mean")

    # Wisconsin Dataset Features - Worst (10 features)
    radius_worst: float = Field(description="Worst (largest) radius value")
    texture_worst: float = Field(description="Worst (largest) texture value")
    perimeter_worst: float = Field(
        description="Worst (largest) perimeter value")
    area_worst: float = Field(description="Worst (largest) area value")
    smoothness_worst: float = Field(
        description="Worst (largest) smoothness value")
    compactness_worst: float = Field(
        description="Worst (largest) compactness value")
    concavity_worst: float = Field(
        description="Worst (largest) concavity value")
    concave_points_worst: float = Field(
        description="Worst (largest) concave_points value")
    symmetry_worst: float = Field(description="Worst (largest) symmetry value")
    fractal_dimension_worst: float = Field(
        description="Worst (largest) fractal_dimension value")

    # Prediction Results
    prediction: str = Field(
        max_length=20,
        description="AI prediction result: 'Benign' or 'Malignant'"
    )
    confidence: float = Field(
        description="Confidence score (0.0 to 1.0)"
    )
    risk_level: str = Field(
        max_length=20,
        description="Risk assessment: 'Low', 'Medium', or 'High'"
    )

    # Metadata
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Prediction timestamp"
    )
    notes: Optional[str] = Field(
        default="",
        max_length=1000,
        description="Additional notes or comments"
    )
