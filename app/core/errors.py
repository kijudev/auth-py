from fastapi import status
from fastapi.requests import Request
from starlette.responses import JSONResponse

# -------------------------------------------------------------------- App Error


class AppError(Exception):
    code: str = "error"
    message: str = "Something went wrong"
    status: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


# >------------------------------------------------------------------ Categories


class BadRequestError(AppError):
    code = "bad_request"
    message = "Bad request"
    status = status.HTTP_400_BAD_REQUEST


class AuthenticationError(AppError):
    code = "not_authenticated"
    message = "Not authenticated"
    status = status.HTTP_401_UNAUTHORIZED


class PermissionDeniedError(AppError):
    code = "permission_denied"
    message = "Permission denied"
    status = status.HTTP_403_FORBIDDEN


class NotFoundError(AppError):
    code = "not_found"
    message = "Not found"
    status = status.HTTP_404_NOT_FOUND


class ConflictError(AppError):
    code = "conflict"
    message = "Conflict"
    status = status.HTTP_409_CONFLICT


# >-------------------------------------------------------------- Error Handlers


async def app_error_handler(_: Request, error: Exception) -> JSONResponse:
    if not isinstance(error, AppError):
        raise error

    return JSONResponse(
        status_code=error.status,
        content={"detail": error.message, "code": error.code},
    )
