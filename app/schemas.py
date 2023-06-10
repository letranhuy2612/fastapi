from datetime import datetime
import json
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime


class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
    url: str

class MetadataBaseSchema(BaseModel):
    bucket_name : Optional[str] = None
    file_path :Optional[str] = None
    box :str
    class_name :str
    object_id : int
    score : int
    owner_id: int| None = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
