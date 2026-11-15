POETRY ?= poetry

.PHONY: install test lint format build clean

install:
	$(POETRY) install --no-interaction

test:
	$(POETRY) run pytest

lint:
	$(POETRY) run ruff check .
	$(POETRY) run black --check .

format:
	$(POETRY) run ruff check --fix .
	$(POETRY) run black .

build:
	$(POETRY) build

clean:
	rm -rf dist build .pytest_cache .ruff_cache .coverage report.json
