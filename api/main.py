from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .db import model
from .db.database import engine
from .router import account
from .utility.exception_handler import ExceptionHandlerMiddleware
import logging

app = FastAPI(title="Technical Assessment")

# create database table
model.Base.metadata.create_all(bind=engine)

# logging config
logger = logging.Logger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    responses = []
    errors = exc.errors()
    for error in errors:
        if error["input"] and error["msg"]:
            responses.append(jsonable_encoder({error["input"]: error["msg"]}))
        elif error["msg"]:
            responses.append(jsonable_encoder({error["msg"]}))
        else:
            responses.append(error["type"])

    logger.error(f"[{__name__}] {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"success": False, "reason": str(responses)}),
    )


app.add_middleware(ExceptionHandlerMiddleware)
app.include_router(account.router, prefix="/account", tags=["account"])
