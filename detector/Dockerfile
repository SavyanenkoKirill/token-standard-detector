FROM python:3.10.5-slim-buster

WORKDIR /detector

ENV POETRY_HOME="/opt/poetry" \
    PYTHONUNBUFFERED=1

ENV PATH="${PATH}:$POETRY_HOME/bin"

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /detector/

RUN poetry config virtualenvs.create false && poetry install
RUN poetry show

#RUN .venv/bin/activate


COPY . .