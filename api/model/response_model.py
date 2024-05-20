from pydantic import BaseModel
from typing import Optional


class InfoRes(BaseModel):
    success: bool
    reason: Optional[str] = None
