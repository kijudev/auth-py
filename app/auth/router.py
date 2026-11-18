from fastapi import APIRouter, Response, status

from app.auth import service
from app.auth.deps import CurrentUserDep, UserSessionTokenDep
from app.auth.models import (
    UserLogin,
    UserPublic,
    UserRegister,
    UserSessionPublic,
    UserSessionTokenPublic,
)
from app.core.config import settings
from app.core.database import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
)
def register(body: UserRegister, db: SessionDep):
    return service.create_user(db, body)


@router.post("/login", response_model=UserPublic)
def login(body: UserLogin, response: Response, db: SessionDep):
    user = service.authenticate_user(db, body)
    token = service.create_session(db, user)

    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=int(settings.session_ttl.total_seconds()),
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
    )

    return user


@router.post("/token", response_model=UserSessionTokenPublic)
def issue_token(body: UserLogin, db: SessionDep):
    user = service.authenticate_user(db, body)
    return UserSessionTokenPublic(token=service.create_session(db, user))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, db: SessionDep, token: UserSessionTokenDep):
    if token:
        service.delete_session(db, token)

    response.delete_cookie(settings.session_cookie_name)


@router.get("/me", response_model=UserPublic)
def me(user: CurrentUserDep):
    return user


@router.get("/me/sessions", response_model=list[UserSessionPublic])
def my_sessions(user: CurrentUserDep):
    return user.sessions
