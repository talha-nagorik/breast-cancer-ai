import uuid

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=100, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    age: Optional[int] = Field(default=0)
    phone: Optional[str] = Field(default="", max_length=20)
    emergency_contact: Optional[str] = Field(default="", max_length=100)
    blood_type: Optional[str] = Field(default="O+", max_length=5)
    allergies: Optional[str] = Field(default="", max_length=500)
    medications: Optional[str] = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)

class MedicalRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    date: str = Field(max_length=20)
    type: str = Field(max_length=100)
    result: str = Field(max_length=100)
    doctor: str = Field(max_length=100)
    notes: str = Field(max_length=1000)
    status: str = Field(max_length=20, default="pending")
    status_color: str = Field(max_length=10, default="#f59e0b")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FamilyHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    relation: str = Field(max_length=50)
    age: int
    condition: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Session(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(hour=23, minute=59, second=59))
    is_active: bool = Field(default=True)

# New model for breast cancer predictions
class BreastCancerPrediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    
    # Core features from Wisconsin dataset
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float
    
    # Prediction results
    prediction: str = Field(max_length=20)  # "Benign" or "Malignant"
    confidence: float  # Confidence score (0-1)
    risk_level: str = Field(max_length=20)  # "Low", "Medium", "High"
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = Field(default="", max_length=1000)
