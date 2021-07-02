from pydantic import BaseModel as SchemaModel, validator, EmailStr, root_validator
from .models import User



class Login(SchemaModel):
    email: EmailStr
    password: str


    @validator('password')
    def correct_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("incorrect password")
        return v

    @root_validator
    def valid_user(cls, values):
        try:
            User.authenticate(**values)
        except Exception:
            raise ValueError("not user")
        return values







