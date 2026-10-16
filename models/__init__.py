from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True

class BoneDensityInput(BaseModel):
    age: int
    weight_kg: float
    height_cm: float
    gender: Gender

class BoneDensityResult(BaseModel):
    t_score: float
    interpretation: str
    bmi: float
    risk_category: str

class BoneDensityInput(BaseModel):
    age: int
    weight_kg: float
    height_cm: float
    gender: Gender
    activity_level: str = "sedentary" # sedentary, moderate, active
