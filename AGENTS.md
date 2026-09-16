# Working in this starter

- Follow `README.md` for the pinned runtime versions and base startup commands.
- Keep the bare starter database-free. Add persistence only when requested, following `.neander/blocks/postgres/README.md` and copying its examples into ordinary project files.
- Local database work can use system PostgreSQL or the optional `compose.dev.yaml` example; it does not require managed Neon. Keep local connection values in gitignored `.env.local`.
- Apply migrations explicitly, then use `scripts/check-addon-crud.py` before and after an app restart. Keep existing data; do not automatically reset databases or remove volumes.
- Preserve `.neander/compose.yaml` as the production recipe with provisioned Neon metadata. Local persistence checks do not prove managed Neon or production deployment readiness.

When adding database/auth capabilities, merge the block's complete `.neander/compose.yaml.example` in the same change. Read `docs/deployment-contract.md`; preserve the static-valid recipe fast path. Include explicit `provider: null` for user/generated requirements. Keep the public health endpoint available. Do not invent a Neon-hostname guard for a generic PostgreSQL block or weaken existing application-specific restrictions. Always scope local Docker Compose with an explicit unique `-p` and `-f`.
