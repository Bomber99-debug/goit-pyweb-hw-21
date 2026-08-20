FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir "poetry>=2,<3"

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY part_two/quotes_and_authors/ ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]