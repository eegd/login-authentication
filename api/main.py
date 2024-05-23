from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .db import model
from .db.database import engine
from .model.response_model import InfoRes
from .router import auth, user
from .utility.exception import ExceptionHandlerMiddleware
import logging, sys

app = FastAPI(title="Login Authentication")

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# create database table
model.Base.metadata.create_all(bind=engine)
logger.info(f"[{__name__}] MySQL server is connected.")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
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
        content=jsonable_encoder(InfoRes(success=False, reason=str(responses))),
    )


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    client = request.client
    method = request.method
    url = request.url
    logger.info(f"client: {client}, method: {method}, url: {url}")
    response = await call_next(request)
    return response


app.add_middleware(ExceptionHandlerMiddleware)
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(user.router, prefix="/api/v1", tags=["user"])
