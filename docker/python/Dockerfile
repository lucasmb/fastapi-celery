
FROM python:3.10.4-slim-bullseye as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.4-slim-bullseye

WORKDIR /code

#celery worker
COPY ./docker/python/worker-start.sh /code/start-celeryworker
RUN sed -i 's/\r$//g' /code/start-celeryworker
RUN chmod +x /code/start-celeryworker

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt 
COPY --from=requirements-stage /tmp/pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]