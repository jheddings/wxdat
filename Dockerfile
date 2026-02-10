FROM python:3.13

COPY --from=ghcr.io/astral-sh/uv:0.10.1 /uv /uvx /usr/local/bin/
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY src uv.lock pyproject.toml README.md /app/
RUN uv sync --locked --no-dev

# commands must be presented as an array, otherwise it will be launched
# using a shell, which causes problems handling signals for shutdown (#15)
ENTRYPOINT ["python", "-m", "wxdat"]

# allow local callers to change the config file
CMD ["--config=/etc/wxdat.yaml"]
