# Auth system in FastAPI and SQLModel

Simple session auth system using FastAPI and SQLModel.

Sessions are opaque random tokens. Only their BLAKE3 hash is stored, in the
`user_sessions` table. Passwords are hashed with Argon2.

A token can be sent either way; protected routes accept both:

- **Cookie** — `POST /auth/login` sets an `HttpOnly` cookie (browsers).
- **Header** — `POST /auth/token` returns the token in the body; send it as
  `Authorization: Bearer <token>` (API clients). A sent header takes
  precedence over the cookie.

## Endpoints

| Method | Path                | Description                          |
| ------ | ------------------- | ------------------------------------ |
| POST   | `/auth/register`    | Create a user                        |
| POST   | `/auth/login`       | Log in, set session cookie           |
| POST   | `/auth/token`       | Log in, return bearer token          |
| POST   | `/auth/logout`      | Revoke the current session           |
| GET    | `/auth/me`          | Current user                         |
| GET    | `/auth/me/sessions` | Current user's sessions              |

## Layout

```
app/
  core/    config (pydantic-settings), db engine/session, errors,
           password + token hashing, shared model fields
  auth/    models, service (business logic), deps, router, errors
migrations/  Alembic (autogenerate from SQLModel.metadata)
```

## Development

```
cp .env.example .env
just install
just migrations-apply
just dev
```

`just check` runs ruff and ty. Settings come from environment variables or
`.env` (read from the current working directory), see `.env.example`.

New models must be imported in `migrations/env.py` so autogenerate sees them.
