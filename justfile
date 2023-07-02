default: podman_run wait run_migrations api

wait:
    sleep 3

podman_run:
    podman-compose up -d

podman_stop:
    podman-compose down

docker_run:
    docker compose up -d

docker_stop:
    docker compose down

run_migrations:
    alembic -c python_starter_project/database/alembic.ini upgrade head

api:
    uvicorn python_starter_project.api.main:app --reload

test:
    pytest

coverage:
    pytest --cov --cov-report term --cov-report html

html:
    xdg-open htmlcov/index.html
