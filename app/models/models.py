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
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))
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
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

class FamilyHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    relation: str = Field(max_length=50)
    age: int
    condition: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

class Session(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(hour=23, minute=59, second=59))
    is_active: bool = Field(default=True)
