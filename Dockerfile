FROM --platform=linux/amd64 python:3.10-slim as base

FROM base as builder

RUN apt update -y && apt upgrade -y && apt install curl -y
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 -

WORKDIR /usr/src/app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN $HOME/.local/bin/poetry config virtualenvs.create false
RUN $HOME/.local/bin/poetry install --only main
RUN $HOME/.local/bin/poetry export -f requirements.txt --without-hashes >> requirements.txt

FROM base

WORKDIR /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

# disable access logs
ENV ACCESS_LOG=""

ENV APP_MODULE="api_python.app.main:app"
ENV PORT=8080

COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_python api_python
CMD uvicorn $APP_MODULE --host 0.0.0.0 --port $PORT