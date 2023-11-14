from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, description="The user's email address", max_length=255)
    username: str = Field(..., description="The user's username", pattern=r'^\w+$', min_length=3, max_length=255)
    display_name: Optional[str] = Field(None, description="The user's display name", min_length=3, max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., description="The user's password", min_length=8, max_length=255)
    password2: str = Field(..., description="Repeat of the user's password", min_length=8, max_length=255)

    @field_validator("password2")
    def passwords_match(cls, v, values: FieldValidationInfo, **kwargs):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("passwords do not match")
        return v


class UserUpdate(BaseModel):
    new_email: Optional[EmailStr] = Field(None, description="The user's new email address", max_length=255)
    new_display_name: Optional[str] = Field(None, description="The user's new display name", min_length=3,
                                            max_length=255)
    new_username: Optional[str] = Field(None, description="The user's new username", pattern=r'^\w+$', min_length=3,
                                        max_length=255)
    new_password: Optional[str] = Field(None, description="The new password for the user", min_length=8, max_length=255)
    new_password2: Optional[str] = Field(None, description="Repeat of the new password for the user", min_length=8,
                                         max_length=255)
    is_active: Optional[bool] = Field(None, description="Set false to deactivate the user")

    @field_validator("new_password2")
    def passwords_match(cls, v, values: FieldValidationInfo, **kwargs):
        if "new_password" in values.data and v != values.data["new_password"]:
            raise ValueError("passwords do not match")
        return v


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True
