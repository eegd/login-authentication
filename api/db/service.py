from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import model
from .schema import IUser
from ..model.response_model import InfoRes
import logging


class UserService:
    logger = logging.getLogger(__name__)

    def create_user(
        self, user_name: str, user_password: str, db: Session
    ) -> Column[int] | JSONResponse:
        try:
            self.logger.info(
                f"[{__name__}] username: {user_name}, password: {user_password}"
            )
            new_user = model.User(username=user_name, password=user_password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user.id
        except IntegrityError as err:
            # E1062: duplicate key
            error_key = err.orig.args[0]  # type: ignore
            if error_key == 1062:
                self.logger.error(f"[{__name__}] {err.args}")
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=jsonable_encoder(
                        InfoRes(success=False, reason="User is already existed")
                    ),
                )
            else:
                self.logger.error(f"[{__name__}] {err}")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=jsonable_encoder(
                        InfoRes(success=False, reason="Internal Server Error")
                    ),
                )

    def get_user(self, user_name: str | None, db: Session) -> IUser | JSONResponse:
        try:
            user = db.query(model.User).filter(model.User.username == user_name).first()
            if not user:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=jsonable_encoder(
                        InfoRes(success=False, reason="User not found")
                    ),
                )
            return user
        except Exception as err:
            self.logger.error(f"[{__name__}] {err}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(
                    InfoRes(success=False, reason="Internal Server Error")
                ),
            )

    def update_user(
        self, user_id: int, user_retry: int, db: Session
    ) -> int | JSONResponse:
        try:
            edited_user = (
                db.query(model.User)
                .filter(model.User.id == user_id)
                .update({"retry": user_retry})
            )
            db.commit()
            return edited_user
        except Exception as err:
            self.logger.error(f"[{__name__}] {err}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(
                    InfoRes(success=False, reason="Internal Server Error")
                ),
            )
