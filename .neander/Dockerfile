FROM node:24-bookworm-slim AS frontend
WORKDIR /app
RUN npm install -g pnpm@11.18.0
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY tsconfig.json vite.config.ts ./
COPY frontend ./frontend
RUN pnpm build

FROM ghcr.io/astral-sh/uv:0.12.10 AS uv
FROM python:3.13-slim-bookworm
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY app.py ./
COPY --from=frontend /app/dist ./dist
COPY .neander/entrypoint.sh /entrypoint.sh
RUN useradd --create-home app
USER app
ENV PORT=8080
EXPOSE 8080
ENTRYPOINT ["sh", "/entrypoint.sh"]
CMD ["/app/.venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
