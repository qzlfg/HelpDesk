# HelpDesk API

## Stack

- **FastAPI** + **SQLModel** (async SQLAlchemy + Pydantic)
- **AsyncPG** → PostgreSQL, **Valkey** via `redis-py`
- **Alembic** (async migrations), **FastStream[redis]** (message queue)
- **Passlib[bcrypt]** + **PyJWT** (HS256, 7-day tokens)
- Python 3.14, managed via `uv`

## Project layout

```
app/
  main.py              # FastAPI app factory (create_app())
  core/                # config, database, security, dependencies, redis_client
  api/v1/              # versioned route modules
  api/workers/         # FastStream consumer stubs (empty)
  models/              # SQLModel table models (with Enum, Relationship)
  schemas/             # Pydantic request/response schemas
  repositories/        # data access layer (AsyncSession-based CRUD)
  services/            # business logic
  use_cases/           # orchestration (sparse)
alembic/               # async-compatible migrations (env.py)
```

## Architecture conventions

- **Repository → Service → (use_case) → API**: repos inject `AsyncSession`, services inject repos, FastAPI `Depends()` wires everything in `dependencies.py`
- **Enum columns in PostgreSQL require an explicit `name`** in `Column(Enum(..., name="..."))` — Alembic will fail without it
- **Auth**: JWT `sub` = str(user_id), `oauth2_scheme` at `/api/v1/auth/login`
- **Session management**: `async_sessionmaker(expire_on_commit=False)`, session per request via `get_async_session()` generator
- **Repository `create`/`update`** uses `session.flush()` + `session.refresh()`, not commit (caller owns the transaction)

## Commands

```sh
# Full stack (Docker Compose)
docker-compose up --build

# Migrations (no Makefile despite README mentioning `make *`)
alembic revision --autogenerate -m "description"
alembic upgrade head

# Run app directly
uv run uvicorn app.main:app --reload
```

## Known issues

- `app/core/redis_client.py:3` has a broken relative import — `from config import settings` should be `from .config import settings`
- **No Makefile** exists despite README referencing `make up` / `make down` / `make makemigrations` / `make migrate`
- **No tests** exist yet (zero test files in the repo)
- **No linter, formatter, or type checker** configured in pyproject.toml
