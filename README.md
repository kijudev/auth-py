# Auth system in FastAPI and SQLModel

A simple session auth system built with FastAPI and SQLModel.

Sessions are opaque random tokens. Only their BLAKE3 hash is stored in the
`user_sessions` table, so a leaked database doesn't leak working sessions.
Passwords are hashed with Argon2.

## Features

- Register, log in and log out with email and password
- Log in with a cookie (browsers) or a bearer token (API clients)
- Sessions expire after a configurable TTL (7 days by default)
- List the current user's active sessions
- Login takes the same time whether or not the email exists, so it doesn't
  reveal which emails are registered
- Emails are lowercased, so `Foo@x.com` and `foo@x.com` are the same account
- Errors come back in one shape: `{"detail": "...", "code": "..."}`
- Database migrations with Alembic

## API

| Method | Path                | Description                               |
| ------ | ------------------- | ----------------------------------------- |
| POST   | `/auth/register`    | Create a user                             |
| POST   | `/auth/login`       | Log in and set the session cookie         |
| POST   | `/auth/token`       | Log in and get a bearer token in the body |
| POST   | `/auth/logout`      | Delete the current session                |
| GET    | `/auth/me`          | Get the current user                      |
| GET    | `/auth/me/sessions` | List the current user's sessions          |

Protected routes accept either the session cookie or an
`Authorization: Bearer <token>` header. If both are sent, the header wins.

Interactive docs are at `/docs` when the server is running.

## Getting started

You need Python 3.14, [uv](https://docs.astral.sh/uv/) and
[just](https://github.com/casey/just). With Nix, `nix develop` gives you all
of them.

```sh
cp .env.example .env
just install
just migrations-apply
just dev
```

## Configuration

Set these in `.env`:

| Variable                | Default              | Description                          |
| ----------------------- | -------------------- | ------------------------------------ |
| `DATABASE_URL`          | `sqlite:///./app.db` | Database connection URL              |
| `SESSION_COOKIE_NAME`   | `session_token`      | Name of the session cookie           |
| `SESSION_TTL`           | `P7D`                | Session lifetime (ISO 8601 duration) |
| `SESSION_COOKIE_SECURE` | `false`              | Send the cookie over HTTPS only      |

## Commands

| Command                        | Description                      |
| ------------------------------ | -------------------------------- |
| `just dev`                     | Run the dev server               |
| `just migrations-create "msg"` | Generate a new migration         |
| `just migrations-apply`        | Apply migrations                 |
| `just check`                   | Lint, format check and typecheck |
| `just fix`                     | Fix lint and formatting          |
| `just test`                    | Run tests                        |
