from datetime import datetime, timedelta, timezone
from fastapi import status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated
from ..db.service import UserService
from ..model.response_model import InfoRes, InfoUser
from ..utility.config import GlobalConfig as cfg
from ..utility.utils import get_db
import jwt, logging


class AuthService:
    logger = logging.Logger(__name__)
    oauth2_schema = OAuth2PasswordBearer(tokenUrl=cfg.TOKEN_URL)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = cfg.ACCESS_TOKEN_EXPIRE_MINUTES
        self.SECRET_KEY = cfg.SECRET_KEY
        self.crud = UserService()

    def create_access_token(self, data: dict, expires_delta: timedelta | None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_schema)],
        db: Session = Depends(get_db),
    ) -> InfoUser | JSONResponse:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        username = payload.get("sub")
        if not username:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=jsonable_encoder(
                    InfoRes(success=False, reason="Could not validate credentials")
                ),
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = self.crud.get_user(username, db)
        if isinstance(user, JSONResponse):
            return user
        return InfoUser(username=user.username)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
