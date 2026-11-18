from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.core.errors import (
    AppError,
    app_error_handler,
)

api = FastAPI()
api.add_exception_handler(AppError, app_error_handler)
api.include_router(auth_router)


@api.get("/")
async def root():
    return {"message": "Hello World"}
