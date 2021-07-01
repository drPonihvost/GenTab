from pydantic import BaseModel, validator
import validate_email


class Login(BaseModel):
    username: str
    password: str

    # @validator('username')
    # def correct_email(cls, v):
    #     assert validate_email(v), "incorrect email"
    #     return v

