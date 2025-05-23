default: docker_run wait run_migrations api

wait:
    sleep 3

docker_run:
    docker compose up -d

docker_stop:
    docker compose down

run_migrations:
    uv run alembic -c python_starter_project/database/alembic.ini upgrade head

api:
    uv run -- fastapi dev python_starter_project/api/main.py

test:
    uv run pytest

coverage:
    uv run pytest --cov --cov-report term --cov-report html

html:
    xdg-open htmlcov/index.html
