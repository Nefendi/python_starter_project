default: docker_run wait run_migrations api

wait:
    sleep 3

docker_run:
    docker compose up -d

docker_stop:
    docker compose down

run_migrations:
    uv run alembic upgrade head

api:
    uv run -- fastapi dev python_starter_project/api/main.py

test_all:
    uv run pytest -n auto

test_fast:
    uv run pytest -m "not slow" -n auto

test_slow:
    uv run pytest -m slow -n auto

coverage:
    uv run pytest --cov --cov-report term --cov-report html -n auto

html:
    xdg-open htmlcov/index.html
