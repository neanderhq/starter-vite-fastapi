# Working in this starter

- Follow `README.md` for the pinned runtime versions and base startup commands.
- Keep the bare starter database-free. Add persistence only when requested, following `.neander/blocks/postgres/README.md` and copying its examples into ordinary project files.
- Local database work can use system PostgreSQL or the optional `compose.dev.yaml` example; it does not require managed Neon. Keep local connection values in gitignored `.env.local`.
- Apply migrations explicitly, then use `scripts/check-addon-crud.py` before and after an app restart. Keep existing data; do not automatically reset databases or remove volumes.
- Preserve `.neander/compose.yaml` as the production recipe with provisioned Neon metadata. Local persistence checks do not prove managed Neon or production deployment readiness.
