from datetime import date, datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Category(str, Enum):
    food = "Food"
    transport = "Transport"
    rent = "Rent"
    utilities = "Utilities"
    entertainment = "Entertainment"
    health = "Health"
    shopping = "Shopping"
    other = "Others"


# ---------- Users ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=100)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)

    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    amount: float = Field(gt=0, le=10_000_000)
    category: Category = Field(default=Category.other, validate_default=True)
    expense_date: date = Field(default_factory=date.today)


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    amount: float
    category: Category
    expense_date: date
    created_at: datetime
    user_id: int

class ExpenseUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    amount: Optional[float] = Field(default=None, gt=0, le=10_000_000)
    category: Optional[Category] = None
    expense_date: Optional[date] = None