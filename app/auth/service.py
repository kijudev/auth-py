from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.auth.errors import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.auth.models import (
    User,
    UserLogin,
    UserRegister,
    UserSession,
)
from app.core.config import settings
from app.core.security import (
    DUMMY_PASSWORD_HASH,
    Token,
    generate_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.core.time import now_utc

# >------------------------------------------------------------------------ User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.exec(select(User).where(User.email == email)).first()


def create_user(db: Session, register: UserRegister) -> User:
    if get_user_by_email(db, register.email):
        raise EmailAlreadyRegisteredError

    user = User.model_validate(
        register, update={"password_hash": hash_password(register.password)}
    )

    db.add(user)

    # A concurrent request registered the same email after our check.
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegisteredError from None

    db.refresh(user)
    return user


def authenticate_user(db: Session, login: UserLogin) -> User:
    user = get_user_by_email(db, login.email)

    if user is None:
        verify_password(login.password, DUMMY_PASSWORD_HASH)
        raise InvalidCredentialsError
    if not verify_password(login.password, user.password_hash):
        raise InvalidCredentialsError

    return user


# >---------------------------------------------------------------- User Session


def create_session(db: Session, user: User) -> Token:
    token = generate_session_token()
    session = UserSession(
        token_hash=hash_session_token(token),
        user_id=user.id,
        expires_at=now_utc() + settings.session_ttl,
    )

    db.add(session)
    db.commit()

    return token


def get_valid_session(db: Session, token: Token) -> UserSession | None:
    session = db.get(UserSession, hash_session_token(token))

    if session is None:
        return None
    if session.is_expired():
        db.delete(session)
        db.commit()
        return None

    return session


def delete_session(db: Session, token: Token) -> None:
    session = db.get(UserSession, hash_session_token(token))

    if session is not None:
        db.delete(session)
        db.commit()
