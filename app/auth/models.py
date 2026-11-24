from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, EmailStr, StringConstraints
from sqlmodel import AutoString, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import UTCDateTime

from app.core.fields import (
    CreatedAtField,
    UpdatedAtField,
    UUID4PrimaryField,
)
from app.core.security import TokenHash
from app.core.time import now_utc

# >------------------------------------------------------------------------ User


UserPassword = Annotated[str, StringConstraints(min_length=8, max_length=256)]
UserName = Annotated[str, StringConstraints(min_length=4, max_length=256)]
UserEmail = Annotated[EmailStr, AfterValidator(str.lower)]


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: UUID = UUID4PrimaryField()
    name: UserName
    email: UserEmail = Field(unique=True, index=True, max_length=255)
    password_hash: str
    created_at: datetime = CreatedAtField()
    updated_at: datetime = UpdatedAtField()

    sessions: list[UserSession] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class UserRegister(SQLModel):
    name: UserName
    email: UserEmail
    password: UserPassword


class UserLogin(SQLModel):
    email: UserEmail

    # No min_length: a stricter signup policy must not lock out old passwords.
    password: Annotated[str, StringConstraints(max_length=256)]


class UserPublic(SQLModel):
    id: UUID
    name: UserName
    email: UserEmail
    created_at: datetime
    updated_at: datetime


# >---------------------------------------------------------------- User Session


class UserSession(SQLModel, table=True):
    __tablename__ = "user_sessions"  # type: ignore

    token_hash: TokenHash = Field(
        primary_key=True, sa_type=AutoString(length=64)
    )
    user_id: UUID = Field(
        foreign_key="users.id", ondelete="CASCADE", index=True
    )

    created_at: datetime = CreatedAtField()
    expires_at: datetime = Field(sa_type=UTCDateTime())

    user: User = Relationship(back_populates="sessions")

    def is_expired(self) -> bool:
        return now_utc() > self.expires_at


class UserSessionPublic(SQLModel):
    user_id: UUID
    created_at: datetime
    expires_at: datetime


class UserSessionTokenPublic(SQLModel):
    token: str
    kind: str = "bearer"
