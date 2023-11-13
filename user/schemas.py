from pydantic import BaseModel, EmailStr, Field, field_validator, constr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional

class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, description="The user's email address", max_length=255)
    username: str = Field(..., description="The user's username", pattern=r'^\w+$', min_length=3, max_length=255)
    display_name: Optional[str] = Field(None, description="The user's display name", min_length=3, max_length=255)

class UserCreate(UserBase):
    password: constr(min_length=8) = Field(..., description="The user's password", min_length=8, max_length=255)
    password2: constr(min_length=8) = Field(..., description="Repeat of the user's password", min_length=8, max_length=255)

    @field_validator("password2")
    def passwords_match(cls, v, values: FieldValidationInfo, **kwargs):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("passwords do not match")
        return v

# TODO: add a UserUpdate model


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
