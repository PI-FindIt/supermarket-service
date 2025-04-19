FROM python:3.13-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV ENV development

WORKDIR /supermarket-service

RUN apk add --no-cache patch && pip install --no-cache uv uvicorn



COPY uv.lock pyproject.toml ./
COPY patches/ ./patches/
RUN uv sync --group dev

WORKDIR /supermarket-service/.venv/lib/python3.13/site-packages

RUN patch -p1 < /supermarket-service/patches/strawberry-sqlalchemy.patch

WORKDIR /supermarket-service
EXPOSE 8000
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
