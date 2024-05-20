from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .db import model
from .db.database import engine
from .router import account
from .utility.exception import ExceptionHandlerMiddleware
import logging, sys

app = FastAPI(title="Login Authentication")

# create database table
model.Base.metadata.create_all(bind=engine)

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


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
        content=jsonable_encoder({"success": False, "reason": str(responses)}),
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
app.include_router(account.router, prefix="/account", tags=["account"])
