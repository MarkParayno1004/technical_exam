import logging
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.addresses import router as addresses_router
from app.core.config import get_settings
from app.core.exceptions import AddressNotFoundError, DatabaseError
from app.core.logging import setup_logging
from app.models.database import init_db

setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Production-ready address book API with CRUD and proximity search.",
    version="1.0.0",
)

app.include_router(addresses_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    logger.info("Incoming %s %s", request.method, request.url.path)
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "Completed %s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    logger.info("Application started: %s", settings.app_name)


@app.exception_handler(AddressNotFoundError)
async def address_not_found_handler(_request: Request, exc: AddressNotFoundError):
    logger.error("Address not found: id=%s", exc.address_id)
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(_request: Request, exc: DatabaseError):
    logger.error("Database error: %s", exc.message)
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(_request: Request, exc: SQLAlchemyError):
    logger.error("Unhandled SQLAlchemy error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred"},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_request: Request, exc: RequestValidationError):
    logger.error("Validation error: %s", exc.errors())
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    logger.error("Bad request: %s", exc)
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.get("/", summary="Health check", description="Simple health check endpoint.")
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
