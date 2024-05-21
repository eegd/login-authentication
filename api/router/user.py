from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..auth.auth import AuthService
from ..db.service import UserService
from ..model.response_model import InfoRes
from ..model.request_model import UserCreate, UserVerify
from ..utility.utils import get_db
from ..utility.config import MAX_RETRY


auth = AuthService()
crud = UserService()
router = APIRouter()


@router.post(
    "/create",
    response_model=InfoRes,
    status_code=status.HTTP_201_CREATED,
    response_description="Create new user",
)
def create(payload: UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(payload.password)
    id = crud.create_user(payload.username, hashed_password, db)
    if isinstance(id, int):
        return jsonable_encoder({"success": True, "reason": None})
    return id


@router.post(
    "/verify",
    response_model=InfoRes,
    status_code=status.HTTP_200_OK,
    response_description="Verify user",
)
def verify(payload: UserVerify, db: Session = Depends(get_db)):
    user = crud.get_user(payload.username, db)
    if isinstance(user, JSONResponse):
        return user

    if user.retry > (int(MAX_RETRY) - 1):
        duration_time = datetime.now().replace(microsecond=0) - user.updated_at  # type: ignore
        if duration_time < timedelta(hours=8, seconds=60):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=jsonable_encoder(
                    {
                        "success": False,
                        "reason": "Please wait one minute before attempting to verify the password again",
                    }
                ),
            )
        else:
            id = crud.update_user(user.id, 0, db)
            if isinstance(id, JSONResponse):
                return id

    valid_password = auth.verify_password(payload.password, user.password)
    if not valid_password:
        user.retry += 1
        id = crud.update_user(user.id, user.retry, db)
        if isinstance(id, JSONResponse):
            return id
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(
                {"success": False, "reason": "Incorrect Password"}
            ),
        )
    else:
        id = crud.update_user(user.id, 0, db)
        if isinstance(id, JSONResponse):
            return id
        return {"success": True, "reason": None}
