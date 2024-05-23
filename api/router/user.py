from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..auth.auth import AuthService
from ..db.service import UserService
from ..model.request_model import UserCreate
from ..model.response_model import InfoRes, InfoUser
from ..utility.utils import get_db


auth = AuthService()
crud = UserService()
router = APIRouter(prefix="/user")


@router.post(
    "/create",
    response_model=InfoRes,
    status_code=status.HTTP_201_CREATED,
    response_description="Create new user",
)
async def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(payload.password)
    id = crud.create_user(payload.username, hashed_password, db)
    if isinstance(id, int):
        return InfoRes(success=True, reason=None)
    return id


@router.get(
    "/me",
    response_model=InfoRes | InfoUser,
    status_code=status.HTTP_200_OK,
    response_description="Read user",
)
async def read_user(current_user: Annotated[InfoUser, Depends(auth.get_current_user)]):
    return current_user
