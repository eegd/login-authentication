from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ..auth.auth import AuthService
from ..db.service import UserService
from ..model.response_model import InfoRes, Token
from ..utility.config import GlobalConfig as cfg
from ..utility.utils import get_db


auth = AuthService()
crud = UserService()
router = APIRouter(prefix="/auth")


@router.post(
    "/token",
    response_model=InfoRes | Token,
    status_code=status.HTTP_200_OK,
    response_description="Login for token",
)
async def login_for_token(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = crud.get_user(payload.username, db)
    if isinstance(user, JSONResponse):
        return user

    if user.retry > (int(cfg.LOGIN_MAX_RETRY) - 1):
        duration_time = datetime.now().replace(microsecond=0) - user.updated_at  # type: ignore
        if duration_time < timedelta(hours=8, seconds=60):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=jsonable_encoder(
                    InfoRes(
                        success=False,
                        reason="Please wait one minute before attempting to verify the password again",
                    ),
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
                InfoRes(success=False, reason="Incorrect Password")
            ),
        )
    else:
        id = crud.update_user(user.id, 0, db)
        if isinstance(id, JSONResponse):
            return id
        access_token_expires = timedelta(minutes=int(cfg.ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
