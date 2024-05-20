from datetime import date
from pydantic import BaseModel


class IUser(BaseModel):
    id: int
    username: str
    password: str
    retry: int
    created_at: date
    updated_at: date
