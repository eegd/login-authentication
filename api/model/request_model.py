from pydantic import BaseModel, Field, field_validator
import re


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=3, max_length=32)

    @field_validator("password")
    def validate_password(cls, value):
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$")
        if not pattern.match(value):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one number"
            )
        return value
