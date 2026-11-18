# Auth system in FastAPI and SQLModel

Simple session auth system using FastAPI and SQLModel. Sessions are opaque random tokens. Only their BLAKE3 hash is stored, in the
`user_sessions` table. Passwords are hashed with Argon2.
