"""
Data models for the Slalom Capabilities Management System
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegistration(BaseModel):
    """Model for user registration request"""
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters")
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)


class UserLogin(BaseModel):
    """Model for user login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Model for user response (without password)"""
    email: str
    first_name: str
    last_name: str
    created_at: str


class TokenResponse(BaseModel):
    """Model for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class CapabilityRegistration(BaseModel):
    """Model for capability registration request (no longer needs email in body)"""
    pass  # Email comes from authenticated user
