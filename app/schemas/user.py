from typing import Optional, Dict, Any

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo


class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, description="The user's email address", max_length=255)
    username: str = Field(..., description="The user's username", pattern=r'^\w+$', min_length=3, max_length=255)
    display_name: Optional[str] = Field(None, description="The user's display name", min_length=3, max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., description="The user's password", min_length=8, max_length=255)


class UserUpdate(BaseModel):
    new_email: Optional[EmailStr] = Field(None, description="The user's new email address", max_length=255)
    new_display_name: Optional[str] = Field(None, description="The user's new display name", min_length=3,
                                            max_length=255)
    new_username: Optional[str] = Field(None, description="The user's new username", pattern=r'^\w+$', min_length=3,
                                        max_length=255)
    new_password: Optional[str] = Field(None, description="The new password for the user", min_length=8, max_length=255)

    is_active: Optional[bool] = Field(None, description="Set false to deactivate the user")






class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True
