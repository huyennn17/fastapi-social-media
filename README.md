# FastAPI Social Media

A REST API for user registration, JWT authentication, posts, and per-user voting on posts, backed by PostgreSQL.

## 1. Project Title

**FastAPI Social Media** — see the heading above for the project name and one-line description.

## 2. Overview

This project is a **backend-only** social-style API. Clients can register users, sign in to receive an access token, create and manage posts, and add or remove votes on posts. Post listings include an aggregated vote count.

**Problem it solves:** it provides a small, self-contained example of a modern Python API with relational data, password hashing, bearer-token auth, and many-to-many-style voting (one vote per user per post).

**Target users:** developers learning or demonstrating FastAPI + SQLAlchemy + PostgreSQL, or teams using this as a starting template for a minimal content-and-reactions service. There is **no bundled web frontend** in this repository.

## 3. Features

- User registration with bcrypt-hashed passwords
- OAuth2-compatible login (`/login`) returning a JWT access token
- JWT bearer authentication for protected routes
- CRUD-style operations on posts (list with pagination and title search, get by id, create, update, delete)
- Post ownership: only the author can update or delete a post
- Voting: authenticated users can add a vote (`dir: 1`) or remove their vote (`dir: 0`) on a post
- Post list and detail responses include a **vote count** (left join + aggregate)
- Database schema managed with **Alembic** migrations
- **Docker Compose** files for local and compose-based deployment
- **GitHub Actions** workflow to install dependencies, run tests, and build/push a Docker image (when configured)

## 4. Tech Stack

| Layer | Technology |
|--------|------------|
| **Frontend** | Not included in this repository. Consume the API with any HTTP client, SPA, or mobile app. |
| **Backend** | Python 3.11, FastAPI, Starlette, Uvicorn |
| **Database** | PostgreSQL, SQLAlchemy 2.x, psycopg2-binary |
| **APIs** | REST (JSON). Interactive docs: `/docs` (Swagger UI) and `/redoc` when the server is running. |
| **Auth** | JWT (`python-jose`), OAuth2 password flow + Bearer token (`fastapi.security`) |
| **Deployment** | Dockerfile, Docker Hub push via GitHub Actions, `docker-compose-dev.yml` / `docker-compose-prod.yml` |
| **Tools** | Alembic (migrations), pytest / httpx (testing), pydantic-settings (configuration) |

> **Note:** The repository does not define a dedicated linter (e.g. Ruff) or formatter in CI; add those manually if you want them enforced.

## 5. Project Structure

```
fastapi-social-media/
├── app/
│   ├── main.py              # FastAPI app instance, CORS, router registration
│   ├── config.py            # Pydantic settings from environment variables
│   ├── database.py          # SQLAlchemy engine, session factory, get_db dependency
│   ├── models.py            # ORM models (User, Post, Vote)
│   ├── schemas.py           # Pydantic request/response models
│   ├── oauth2.py            # JWT creation, verification, get_current_user
│   ├── utils.py             # Password hashing and verification (passlib/bcrypt)
│   └── routers/             # Route handlers grouped by domain
│       ├── auth.py
│       ├── user.py
│       ├── post.py
│       └── vote.py
├── alembic/                 # Migration environment and version scripts
│   ├── env.py
│   └── versions/
├── tests/                   # Pytest suite and fixtures
│   ├── conftest.py
│   ├── test_posts.py
│   ├── test_users.py
│   └── test_votes.py
├── requirements.txt         # Python dependencies (pinned versions)
├── Dockerfile               # Container image for the API
├── docker-compose-dev.yml   # Dev-oriented compose (example env in file)
├── docker-compose-prod.yml  # Compose using host-supplied env vars
├── alembic.ini              # Alembic CLI configuration
└── .github/workflows/       # CI: install, test, Docker build/push
```

- **`app/`** — all application logic: configuration, persistence, security, and HTTP routers.
- **`alembic/`** — database migrations; `env.py` builds the DB URL from the same settings as the app.
- **`tests/`** — automated tests with dependency overrides for the database session.

## 6. Getting Started

### Prerequisites

- Python **3.11** (recommended; matches Dockerfile and CI)
- **PostgreSQL** reachable from your machine (or use Docker Compose)
- `git` and `pip` (or a virtual environment tool)

### Installation

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment (recommended):

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Environment variables

1. Create a `.env` file in the project root (the app loads it via `pydantic-settings`; see `app/config.py`).
2. Set every variable listed in [§7. Environment Variables](#7-environment-variables) using **your own** values (never commit real secrets).

> There is no `.env.example` file in the repository yet; you may add one for your team.

### Run locally

1. Ensure PostgreSQL is running and the database exists.
2. Apply migrations:

   ```bash
   alembic upgrade head
   ```

3. Start the API:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open `http://127.0.0.1:8000/docs` for interactive API documentation.

**Alternative (Docker Compose — development file):** from the repo root, with Docker installed:

```bash
docker compose -f docker-compose-dev.yml up
```

The dev compose file supplies example environment variables; **replace secrets** before any shared or production use.

## 7. Environment Variables

All of the following are **required** by `app/config.py` unless you change the settings model. Use placeholders locally; use strong secrets in production.

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_HOSTNAME` | PostgreSQL host (e.g. `localhost` or service name `postgres` in Docker) | Yes |
| `DATABASE_PORT` | PostgreSQL port (e.g. `5432`) | Yes |
| `DATABASE_PASSWORD` | PostgreSQL user password | Yes |
| `DATABASE_NAME` | Database name | Yes |
| `DATABASE_USERNAME` | PostgreSQL user name | Yes |
| `SECRET_KEY` | Secret key for signing JWTs (use a long random string) | Yes |
| `ALGORITHM` | JWT algorithm (e.g. `HS256`) | Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes (integer) | Yes |

**Example placeholders (not for production):**

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your-db-password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=change-me-to-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **`docker-compose-prod.yml`** maps `DATABASE_HOSTNAME` from a host variable named `POSTGRES_HOSTNAME`. Align your shell or `.env` with that file, or update the compose file manually for consistency.

## 9. Usage

After the server is running:

1. **Register** a user with `POST /users/` (JSON body: email and password).
2. **Log in** with `POST /login` using form fields `username` (your **email**) and `password`. The response contains `access_token` and `token_type` (`bearer`).
3. **Call protected routes** by sending the header: `Authorization: Bearer <access_token>`.
4. **Create posts** with `POST /posts/`. **List posts** with `GET /posts/` (optional query: `limit`, `skip`, `search`). **Vote** with `POST /vote/` (`post_id` and `dir`: `1` to vote, `0` to remove your vote).

**Example workflow (with `curl`):**

```bash
# 1. Register
curl -s -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"your-secure-password"}'

# 2. Login (form-encoded)
curl -s -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=your-secure-password"

# 3. Use token (replace TOKEN)
curl -s http://127.0.0.1:8000/posts/ \
  -H "Authorization: Bearer TOKEN"
```

For day-to-day exploration, **Swagger UI** at `/docs` is the simplest way to authenticate and try endpoints.

## 10. API Documentation

Base URL when running locally: `http://127.0.0.1:8000` (adjust host/port as needed).

### Public routes

| Method | Endpoint | Description | Request body | Response example |
|--------|----------|-------------|--------------|------------------|
| `GET` | `/` | Welcome message | — | `{"message":"Welcome to the FastAPI Social Media App!"}` |
| `POST` | `/users/` | Create a user (password stored hashed) | JSON: `{"email":"user@example.com","password":"string"}` | `{"id":1,"email":"user@example.com","created_at":"2026-01-01T12:00:00+00:00"}` |
| `GET` | `/users/{id}` | Get user by numeric id | — | Same shape as create, without password |
| `POST` | `/login` | OAuth2 password flow; `username` must be the user’s **email** | Form: `username`, `password` | `{"access_token":"<jwt>","token_type":"bearer"}` |

### Protected routes (header: `Authorization: Bearer <token>`)

| Method | Endpoint | Description | Request body | Response example |
|--------|----------|-------------|--------------|------------------|
| `GET` | `/posts/` | List posts with vote counts; query: `limit` (default 10), `skip`, `search` (substring on title) | — | JSON array of objects shaped like `PostOut` (see below) |
| `POST` | `/posts/` | Create a post for the current user | JSON: `{"title":"...","content":"...","published":true}` (`published` optional, default `true`) | Full post including `id`, `created_at`, nested `owner` |
| `GET` | `/posts/{id}` | Get one post with vote count | — | `PostOut` shape |
| `PUT` | `/posts/{id}` | Update post (owner only) | Same JSON as create | Updated post object |
| `DELETE` | `/posts/{id}` | Delete post (owner only) | — | `204 No Content` on success |
| `POST` | `/vote/` | Add vote (`dir: 1`) or remove vote (`dir: 0`) | JSON: `{"post_id":1,"dir":1}` | `{"message":"Vote added successfully"}` or removal message |

**`PostOut` list/detail shape** (nested key is capitalized `Post` in JSON):

```json
{
  "Post": {
    "title": "Hello",
    "content": "World",
    "published": true,
    "id": 1,
    "created_at": "2026-01-01T12:00:00+00:00",
    "owner": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-01-01T12:00:00+00:00"
    }
  },
  "votes": 3
}
```

**Typical error status codes:** `401` invalid or missing token; `403` wrong password, unknown user on login, or not allowed to modify another user’s post; `404` missing post or vote; `409` duplicate vote.

> For exhaustive request/response schemas and “Try it out”, use **`/docs`** at runtime.

## 11. Database

### Main models

- **`users`** — `id`, `email` (unique), `password` (hash), `created_at`.
- **`posts`** — `id`, `title`, `content`, `published`, `created_at`, `owner_id` → `users.id` (on delete cascade).
- **`votes`** — composite primary key (`user_id`, `post_id`) with foreign keys to `users` and `posts` (cascade delete).

Relationships: a post has one owner (`User`); a vote row links one user to one post.

### Migrations

Migrations live under `alembic/versions/`. Alembic reads the database URL from **`app.config.settings`** (same environment variables as the app).

```bash
# Apply all migrations
alembic upgrade head

# Create a new revision after changing models (review autogenerate output)
alembic revision --autogenerate -m "describe change"
```

There is **no seed script** in the repository; use tests, SQL, or a small script if you need sample data.

## 12. Testing

Tests use **pytest**, **httpx** (via Starlette/FastAPI `TestClient`), and fixtures in `tests/conftest.py` that override the `get_db` dependency and recreate tables with SQLAlchemy metadata.

**Run tests** (PostgreSQL must match your env; CI uses a service container and GitHub secrets):

```bash
pytest
```

Optional coverage (packages are present in `requirements.txt`; CI currently runs plain `pytest`):

```bash
pytest --cov=app --cov-report=term-missing
```

> A legacy file `tests/datapase.py` exists with alternate fixtures; the active suite is driven by **`conftest.py`**. Some test functions omit the `test_` prefix and may not be collected—clean up manually if you rely on them.

## 13. Deployment

### Docker image

Build:

```bash
docker build -t your-registry/fastapi-social-media:latest .
```

The Dockerfile runs Uvicorn on port **8000** with **`--reload`**, which is convenient for development; for production you may want to remove `--reload` and run multiple workers (update the Dockerfile manually).

### Docker Compose (production-oriented file)

1. Set required environment variables on the host (see `docker-compose-prod.yml`: database, JWT, and note `POSTGRES_HOSTNAME` for the API’s `DATABASE_HOSTNAME`).
2. Run:

   ```bash
   docker compose -f docker-compose-prod.yml up --build -d
   ```

3. Run **`alembic upgrade head`** against the production database (from a job, init container, or one-off command) so the schema exists.

### GitHub Actions

Workflow **`.github/workflows/build-deploy.yml`**: installs dependencies, runs **`pytest`** against Postgres (requires repository **secrets** for database and JWT settings), then logs in to Docker Hub and **builds and pushes** an image tagged `DOCKER_HUB_USERNAME/fastapi:latest` (exact tag is defined in the workflow file).

> Update image names, tags, and secrets to match your organization’s policy.

*This README was generated to match the repository layout and code at the time of writing. If behavior or paths change, update the relevant sections manually.*
