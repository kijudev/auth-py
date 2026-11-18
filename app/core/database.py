from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlmodel import Session, create_engine

from app.core.config import settings

is_sqlite = settings.database_url.startswith("sqlite")

connect_args = {"check_same_thread": False} if is_sqlite else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


def enable_sqlite_foreign_keys(conn: DBAPIConnection, conn_record):
    # conn - raw DBAPI connection, which is a sqlite3.Connection for SQLite.
    # conn_record - sqlalchemy.pool._ConnectionRecord - connection pool record.
    # SQLite ignores foreign keys (and ON DELETE CASCADE) unless enabled.

    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if is_sqlite:
    event.listen(engine, "connect", enable_sqlite_foreign_keys)


def get_database() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_database)]
