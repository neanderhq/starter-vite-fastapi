# Vite + FastAPI

Use Node 24, pnpm 11.18.0, Python 3.13 and uv 0.12.10. Run `pnpm install --frozen-lockfile` and `uv sync --frozen`. In separate terminals run `pnpm dev:api` (http://127.0.0.1:8000) and `pnpm dev` (http://localhost:5173). Vite proxies relative `/api` requests to FastAPI; no CORS setup is needed. `pnpm build` builds the frontend into `dist/`.

Publish uses `.neander/compose.yaml`. For local production verification, run `docker build -f .neander/Dockerfile -t my-python-app .` and `docker run --rm -p 8080:8080 my-python-app`. FastAPI serves the SPA, `/api/health`, and `/docs`. Define additional API routes before the unknown-API handler. Unknown API routes return JSON 404; frontend routes fall back to the SPA, while missing assets return 404.

No database or authentication is installed. Add these only when requested. Keep callback/backend origins in runtime server configuration and browser API calls relative. Never commit `.env` files with credentials. Stack provenance is in `docs/architecture/stack-decision.md`.

When persistence is requested, follow the [Postgres block's local setup](.neander/blocks/postgres/README.md#local-development): use existing system Postgres or its optional Docker Compose example, apply migrations, and verify CRUD across an app restart. Managed Neon is not needed to build and test locally; production still uses the managed Neon recipe contract.


## Maintenance and verification

This private Neander template repository owns the application, pinned lockfiles, deployment recipe, and [incremental building blocks](add-ons.md). Changes are reviewed here independently of the Neander application. New projects take a one-time copy of a selected commit; starter updates never overwrite existing projects.

Run from this repository root:

```sh
docker build -f .neander/Dockerfile -t neander-starter-vite-fastapi:local .
python3 scripts/test_entrypoint.py
docker run --detach --name starter-check --publish 127.0.0.1:8080:8080 neander-starter-vite-fastapi:local
python3 scripts/smoke.py http://127.0.0.1:8080
docker rm --force starter-check
```

The CI workflow runs these base container checks on every pull request and main push. It requires no cloud credentials or database. After installing a database block, use `python3 scripts/check-addon-crud.py ORIGIN`, restart the disposable app, then repeat with its printed ID to check persistence and delete the test row. Follow the block's README for migrations and authentication checks.

Pinned dependencies, production recipes, and building blocks were preserved during extraction from Neander. Repeat production certification when dependencies or base-image tags change; local container checks do not establish Cloud Run latency or real OAuth-provider login. No open-source license is granted by this private repository.

## Keeping Publish ready

Follow [the deployment contract](docs/deployment-contract.md) when adding database or authentication features. Each block includes a complete production recipe example; merge it in the same change as the implementation. The base starter remains database-free.
