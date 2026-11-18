import uuid

from sqlmodel import Column, Field, func
from sqlmodel.sql.sqltypes import UTCDateTime

from app.core.time import now_utc

# >----------------------------------------------------------------- Date Fields


def CreatedAtField():
    return Field(
        default_factory=now_utc,
        sa_column=Column(
            UTCDateTime(),
            server_default=func.now(),
            nullable=False,
        ),
    )


def UpdatedAtField():
    return Field(
        default_factory=now_utc,
        sa_column=Column(
            UTCDateTime(),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )


# >------------------------------------------------------------------- Id Fields


def UUID4PrimaryField():
    return Field(primary_key=True, default_factory=uuid.uuid4)
