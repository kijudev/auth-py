default:
    @just --list

install:
    uv sync

dev:
    fastapi dev app/main.py

migrations-create message:
    alembic revision --autogenerate -m "{{ message }}"

migrations-apply:
    alembic upgrade head

check:
    ruff check .
    ruff format --check .
    ty check

fix:
    ruff check --fix .
    ruff format .

test:
    pytest
