FROM ghcr.io/astral-sh/uv:python3.13-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV ENV development

WORKDIR /supermarket-service

ENV PATH="/supermarket-service/.venv/bin:$PATH"
RUN apk add --no-cache patch



COPY uv.lock pyproject.toml ./
COPY patches/ ./patches/
RUN uv sync --frozen

WORKDIR /supermarket-service/.venv/lib/python3.13/site-packages

RUN patch -p1 < /supermarket-service/patches/strawberry-sqlalchemy.patch

WORKDIR /supermarket-service
EXPOSE 8000
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
