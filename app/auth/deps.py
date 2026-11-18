from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth import service
from app.auth.models import User
from app.core.config import settings
from app.core.database import SessionDep
from app.core.errors import AuthenticationError
from app.core.security import Token

bearer = HTTPBearer(auto_error=False)

SessionTokenCookie = Annotated[
    Token | None, Cookie(alias=settings.session_cookie_name)
]

SessionTokenBearer = Annotated[
    HTTPAuthorizationCredentials | None, Depends(bearer)
]


def get_session_token(
    cookie_token: SessionTokenCookie = None,
    bearer_credentials: SessionTokenBearer = None,
) -> Token | None:
    if bearer_credentials is not None:
        return Token(bearer_credentials.credentials)

    return cookie_token


UserSessionTokenDep = Annotated[Token | None, Depends(get_session_token)]


def get_current_user(db: SessionDep, token: UserSessionTokenDep) -> User:
    session = service.get_valid_session(db, token) if token else None

    if session is None:
        raise AuthenticationError

    return session.user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
