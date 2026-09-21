from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from doc_processor.api.exception_handlers import (
    app_exception_handler,
    unexpected_exception_handler,
    validation_exception_handler,
)
from doc_processor.api.v1.router import api_router
from doc_processor.exceptions.exceptions import AppException

app = FastAPI()


app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)
app.include_router(api_router)
