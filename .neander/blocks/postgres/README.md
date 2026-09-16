# SQLAlchemy + managed Neon, version 1

Add only when persistence is requested: `uv add sqlalchemy==2.0.52 'psycopg[binary]==3.3.5' alembic==1.19.2 python-dotenv==1.2.3`. Copy each `.example` to its shown project-relative path without that suffix, creating directories and merging existing modules. Add `from server.todos import router as todo_router` and `app.include_router(todo_router)` in `app.py` **before** the unknown `/api` catchall. Add `COPY server ./server` to the production Dockerfile after `COPY app.py ./`.

## Local development

Choose an existing local PostgreSQL database or Docker; managed Neon is not required for local development. The block reads `DATABASE_URL` from the already-gitignored `.env.local`. An exported `DATABASE_URL` takes precedence, so remove any stale export before starting the app or migrations.

For an already-running system PostgreSQL installation, create a project-specific development database using an existing local role with database-creation permission. Replace `YOUR_DEV_USER` and `YOUR_PROJECT_DEV_DATABASE` below with that role and an unused database name; this does not install PostgreSQL or create a role:

```sh
createdb --host=127.0.0.1 --port=5432 --username=YOUR_DEV_USER YOUR_PROJECT_DEV_DATABASE
```

Put its connection URL in `.env.local`, for example `DATABASE_URL=postgresql://YOUR_DEV_USER:YOUR_DEV_PASSWORD@127.0.0.1:5432/YOUR_PROJECT_DEV_DATABASE`, substituting your actual local values and URL-encoding password characters if needed. Do not connect this workflow to a production database.

For Docker, copy the optional example to the repository root only when adding persistence (skip the copy if it is already there):

```sh
cp -n .neander/blocks/postgres/compose.dev.yaml.example compose.dev.yaml
docker compose -p YOUR_UNIQUE_PROJECT -f compose.dev.yaml up -d --wait --wait-timeout 120
```

The database listens only on `127.0.0.1:55432`. If that port is busy, export a free port, such as `export PGPORT=55433`, before running Compose. Add this line to `.env.local`, adjusting the port to match; preserve any other variables already in that file:

```dotenv
DATABASE_URL=postgresql://neander_dev:neander_dev_only@127.0.0.1:55432/neander_dev
```

These are development-only credentials for this local container. Compose scopes the named volume to the explicit project name. Replace `YOUR_UNIQUE_PROJECT` with a stable unique name and select a free `PGPORT` per project; retain both for subsequent commands. No fixed container or volume name is shared across projects.

With the example modules installed, apply migrations and start the API:

```sh
uv run alembic upgrade head
pnpm dev:api
```

Run `pnpm dev` in another terminal. Verify the installed block against the local API:

```sh
python3 scripts/check-addon-crud.py http://127.0.0.1:8000
# Restart pnpm dev:api, then use the ID printed above:
python3 scripts/check-addon-crud.py http://127.0.0.1:8000 PERSISTED_ID
```

This creates, updates and validates a test row; the second command verifies persistence across an app restart and deletes that row. To also verify volume persistence, do the following **before the second check**: stop the app, run `docker compose -p YOUR_UNIQUE_PROJECT -f compose.dev.yaml down`, bring it back with the same `up` command, and restart the app. Then run the second check once with the saved ID. If you already deleted that row, run the first command again to create a new one. `down` preserves the named volume; do not add `--volumes` or automatically reset the database. Local checks establish local persistence, not managed Neon or production deployment readiness.

## Production

Production continues to use managed Neon through Neander's runtime environment bundle. Add the required provisioned Neon `DATABASE_URL` metadata to `x-neander.environment`; keep `compose.dev.yaml` separate from `.neander/compose.yaml`. No production connection belongs on the desktop. A separately attached development Neon connection is also an option, but is not a prerequisite for local work.

Apply the included additive migration explicitly: `uv run alembic upgrade head`. Generate subsequent changes with `uv run alembic revision --autogenerate -m 'description'`, inspect SQL and commit migrations. The isolated production migration action uses `.venv/bin/alembic upgrade head` after installing the locked source dependencies, with only its database credential. Never run migrations during Docker build/startup. PostgreSQL advisory locking and Alembic history prevent duplicate/concurrent application. Automatic destructive downgrades are intentionally unavailable.

Test POST `/api/todos` with `{"title":"Persist me"}`, PATCH `/api/todos/<id>` with `{"done":true}`, restart the server and GET to prove persistence, then DELETE `/api/todos/<id>`. Invalid input must return 422. The example is public until auth is installed; protect private records before exposing them.

Sources: [SQLAlchemy PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html), [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [Compose health waiting](https://docs.docker.com/reference/cli/docker/compose/up/), [Compose volume persistence](https://docs.docker.com/reference/compose-file/volumes/).

Declare `migration: fastapi-alembic` directly under `x-neander` when the migration files are present. Publish then runs that fixed profile in the isolated database-only migration step before application rollout. Do not add arbitrary shell commands to Compose.

## Maintained deployment recipe

This block includes `.neander/compose.yaml.example`, a complete recipe including its database prerequisites. Merge its `x-neander` declarations into the project's `.neander/compose.yaml` as you install the block; do not replace existing services, probes or application-specific requirements. Every environment entry includes `service`, `name`, `required`, `source` and `provider`. The `provider: null` field is mandatory for generated and user-supplied values. Keep the matching migration profile and commit its source files and lockfile in the same change.

Read `docs/deployment-contract.md` before changing database or authentication setup. Keep the public health endpoint accessible when protecting application pages. A valid recipe goes directly to Cloud Run Compose; adding an add-on must not depend on a recipe agent to reconstruct this metadata at Publish time.

Use one stable, unique project name in place of `YOUR_UNIQUE_PROJECT` on **every** Compose command. Always pass both `-p` and `-f`; inherited `COMPOSE_PROJECT_NAME` or `COMPOSE_FILE` must not select another project. Use a different free host port for each concurrently running database.
