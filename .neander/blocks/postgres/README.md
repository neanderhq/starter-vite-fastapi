# SQLAlchemy + managed Neon, version 1

Add only when persistence is requested: `uv add sqlalchemy==2.0.52 'psycopg[binary]==3.3.5' alembic==1.19.2 python-dotenv==1.2.3`. Copy each `.example` to its shown project-relative path without that suffix, creating directories and merging existing modules. Add `from server.todos import router as todo_router` and `app.include_router(todo_router)` in `app.py` **before** the unknown `/api` catchall. Add `COPY server ./server` to the production Dockerfile after `COPY app.py ./`.

Attach the development database through Neander. The block reads its gitignored `.env.local` `DATABASE_URL`; production reads the runtime environment bundle. Add the required provisioned Neon `DATABASE_URL` metadata to `x-neander.environment`. No production connection belongs on the desktop.

Apply the included additive migration explicitly: `uv run alembic upgrade head`. Generate subsequent changes with `uv run alembic revision --autogenerate -m 'description'`, inspect SQL and commit migrations. The isolated production migration action uses `.venv/bin/alembic upgrade head` after installing the locked source dependencies, with only its database credential. Never run migrations during Docker build/startup. PostgreSQL advisory locking and Alembic history prevent duplicate/concurrent application. Automatic destructive downgrades are intentionally unavailable.

Test POST `/api/todos` with `{"title":"Persist me"}`, PATCH `/api/todos/<id>` with `{"done":true}`, restart the server and GET to prove persistence, then DELETE `/api/todos/<id>`. Invalid input must return 422. The example is public until auth is installed; protect private records before exposing them.

Sources: [SQLAlchemy PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html), [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html).

Declare `migration: fastapi-alembic` directly under `x-neander` when the migration files are present. Publish then runs that fixed profile in the isolated database-only migration step before application rollout. Do not add arbitrary shell commands to Compose.
