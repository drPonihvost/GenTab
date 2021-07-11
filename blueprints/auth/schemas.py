from pydantic import BaseModel as SchemaModel, validator, EmailStr, root_validator
from .models import User
from .models import UserError, PasswordError


class Login(SchemaModel):
    email: EmailStr
    password: str

    @root_validator
    def valid_user(cls, values):
        if not values.get("email"):
            return values
        try:
            User.authenticate(**values)
        except UserError:
            raise ValueError("User does not exist")
        except PasswordError:
            raise ValueError("Incorrect password")
        return values


class Registrations(SchemaModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    org_name: str

    @validator('email')
    def validate_email(cls, v: str) -> str:
        user = User.get_email(v)
        if user:
            raise ValueError('This user already exists')
        return v

    @validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("incorrect password")
        return v

    @validator('name')
    def validate_name(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("The field cannot be empty")
        return v

    @validator('surname')
    def validate_surname(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("The field cannot be empty")
        return v

    @validator('org_name')
    def validate_org(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("The field cannot be empty")
        return v
