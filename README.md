# python-starter-project

This is a small template which should be used to start bigger Python-based
projects. It features [Poetry](https://python-poetry.org/) as a packaging and
dependency manager as well as a few development packages defined in the
configuration.

The packages included are:

- black
- flake8_bugbear
- mypy
- pylint
- pylint-pytest
- pytest
- pytest-randomly
- pytest_cov
- assertpy
- pre_commit
- isort

Configurations for the aforementioned tools were defined in the separate files
or, if it was possible, in the **pyproject.toml**.

Configuration for [pre-commit](https://pre-commit.com/) should be defined by the
user.
